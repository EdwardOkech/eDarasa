from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.http import HttpResponseRedirect

from braces.views import GroupRequiredMixin, LoginRequiredMixin

from .forms import LessonQuestionForm
from .models import Course, Module, Lesson, CourseEnrollment, AlreadyEnrolledError, LessonQuestion
from jm_lms.apps.dashboard.views import StudentDashboardCourseView


class CourseListView(ListView):
    model = Course
    context_object_name="course_list"
    template_name='course/course_list.html'
    paginate_by = 10
    
    
class CourseDetailView(DetailView):
    model = Course
    template_name='course/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['module_list'] = Module.objects.filter(course__slug=self.kwargs['course_slug'], status=Module.PUBLISHED)
        return context
  
    
class ModuleListView(ListView):
    model = Module
    context_object_name="module_list"
    template_name='course/module_list.html'
    paginate_by = 10
    
    
class ModuleDetailView(DetailView):
    model = Module
    template_name='course/module_detail.html'
    context_object_name = 'module'
    slug_url_kwarg = 'module_slug'
    
    def get_context_data(self, **kwargs):
        context = super(ModuleDetailView, self).get_context_data(**kwargs)
        context['lesson_list'] = Lesson.objects.filter(module__slug=self.kwargs['module_slug'])
        return context
    
    """def get_object(self):
        return get_object_or_404(Module, pk=request.session['user_id'])"""

        
class LessonCreateView(CreateView):
    model = Lesson
    template_name='course/lesson_create.html'
    fields = ['name', 'content']
    
    def get_context_data(self, **kwargs):
        context = super(LessonCreateView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.get(slug=self.kwargs['module_slug'])
        return context
        
    def get_success_url(self):
        """Redirect to the module detail page"""
        module = Module.objects.get(slug=self.kwargs['module_slug'])
        return reverse('module_detail', args=[self.object.module.course.slug, self.object.module.slug])
        
    def form_valid(self, form):
        """Save the lesson for the selected module."""
        self.object = form.save(commit=False)
        self.object.module = Module.objects.get(slug=self.kwargs['module_slug'])
        self.object.save()
        return super(LessonCreateView, self).form_valid(form)


class LessonDetailView(DetailView):
    model = Lesson
    template_name='course/lesson_detail.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'
    
    
class EnrolUserTemplateView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'dashboard/student_courses.html'
    group_required = u"Student"
    
    def get(self, request, *args, **kwargs):
        student = get_user_model().objects.get(id=kwargs['userid'])
        course = Course.objects.get(id=kwargs['courseid'])
        try:
            enrollment = CourseEnrollment.enroll(student, course)
        except AlreadyEnrolledError:
            pass
        
        #print(kwargs['userid'])
        #kwargs['greeting'] = 'Bonjour'
        return HttpResponseRedirect(reverse('student_courses'))
        #return super(EnrolUserTemplateView, self).get(request, *args, **kwargs) 
                                               
    def get_context_data(self, **kwargs):
        context = super(EnrolUserTemplateView, self).get_context_data(**kwargs)
        print(kwargs['userid'])
        #user = User.objects.get(id=kwargs['userid'])
        #do something with this user
        return context
    
    
def enrol_student_to_course(request, student_id, course_id):
    student = User.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    enrollment = CourseEnrollment.enroll(student, course)
    pass
    
class LessonQuestionCreateView(CreateView):
    #form_class = LessonQuestionForm
    model = LessonQuestion
    template_name='dashboard/ask_lesson_question.html'
    fields = ['title', 'description']

    def get_context_data(self, **kwargs):
        context = super(LessonQuestionCreateView, self).get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        return context

    def get_success_url(self):
        """Redirect to the module detail page"""
        lesson = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        return reverse('student_lesson_questions', args=[])
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.student = self.request.user
        self.object.lesson = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        self.object.save()
        print('Saving form')
        return super(LessonQuestionCreateView, self).form_valid(form)
        
        
def lesson_question_new(request):
    if request.method == "POST":
        form = LessonQuestionForm(request.POST)
        if form.is_valid():
            lesson_question = form.save(commit=False)
            lesson_question.student = request.user
            lesson_question.lesson = None
            lesson_question.save()
            return redirect('learn_lesson', pk=post.pk)
    else:
        form = LessonQuestionForm()    
    return render(request, 'dashboard/ask_lesson_question.html', {'form': form})
