from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from braces.views import GroupRequiredMixin, LoginRequiredMixin

from jm_lms.apps.courses.models import Course, Module, Lesson, CourseEnrollment, LessonQuestion, StudentLessonProgress, NOT_STARTED, IN_PROGRESS, COMPLETED
from jm_lms.apps.exercises.models import ( Exercise, Question, UserAnswer, MultiChoiceQuestion, MultiChoiceQuestionOption, MultiChoiceUserSubmittedAnswer, EssayQuestion, EssayUserAnswer,
TableExerciseUserAnswer, TableExerciseQuestion )
from jm_lms.apps.askaquestion.forms import AskQuestionForm
from jm_lms.apps.jobs.models import JobPost


class DashboardView(LoginRequiredMixin, TemplateView):
    
    template_name = 'dashboard/dashboard.html'
    login_url = "/login/"
    
    
class EmployerDashboardView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    template_name = 'dashboard/employer_dashboard.html'
    
    # required: Only users from Employer group can access this view
    group_required = u"Employer"
    
    def get_context_data(self, **kwargs):
        context = super(EmployerDashboardView, self).get_context_data(**kwargs)
        context['active_enrollments'] = CourseEnrollment.objects.filter(is_active=True)
        context['my_jobs'] = JobPost.objects.filter(posted_by=self.request.user)
        return context
    
    
class StudentDashboardView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    #template_name = 'dashboard/student_dashboard.html'
    template_name = 'dashboard/returning_user_welcome.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentDashboardView, self).get_context_data(**kwargs)
        context['my_enrollments'] = CourseEnrollment.objects.filter(student=self.request.user)        
        
        all_courses = Course.objects.all().order_by('position_order')
        # Add dynamic fields to courses
        for course in all_courses:
            course.is_accessible = course.is_previous_course_done(self.request.user)  
            course.done_percent = Course.get_student_progress_in_course(self.request.user, course)
            
            if course.done_percent >= 100:
                course.status = "Complete"
            elif (course.done_percent > 0 and course.done_percent <= 99):
                course.status = "In Progress"
            else:
                course.status = "Prerequisite Not Met"
            
        context['all_courses'] = all_courses
        
        # Determine current module
        current_module = StudentLessonProgress.objects.get_student_current_module(self.request.user)
        if current_module:
            current_module.done_percent = Module.get_student_progress_in_module(self.request.user, current_module)        
        context['current_module'] = current_module
        
        return context
        
        
class StudentWelcomeView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    """
    Shown to users who have logged in for the first time
    """
    
    template_name = 'dashboard/first_time_user_welcome.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentWelcomeView, self).get_context_data(**kwargs)
        context['my_enrollments'] = CourseEnrollment.objects.filter(student=self.request.user)
        context['all_courses'] = Course.objects.all().order_by('position_order')
        try:
            context['intro_course'] = Course.objects.get(id=2) # TODO:  There has to be a better way of getting the intro course
        except Course.DoesNotExist:
            # Get the first course if there is no free intro course
            context['intro_course'] = Course.objects.all()[0]
        return context
        

class StudentDashboardCourseView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    template_name = 'dashboard/student_courses.html'
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentDashboardCourseView, self).get_context_data(**kwargs)
        context['my_enrollments'] = CourseEnrollment.objects.filter(student=self.request.user)
        return context
        

class StudentDashboardModuleView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    template_name = 'dashboard/student_modules.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentDashboardModuleView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['course_slug'])        
        
        course_modules = Module.objects.filter(course__slug=self.kwargs['course_slug'], status=Module.PUBLISHED).order_by('position')
        # Add dynamic fields to modules
        for module in course_modules:
            module.is_accessible = module.is_previous_module_done(self.request.user)   
            module.done_percent = Module.get_student_progress_in_module(self.request.user, module)
            
            if module.done_percent >= 100:
                module.status = "Complete"
            elif (module.done_percent > 0 and module.done_percent <= 99):
                module.status = "In Progress"
            else:
                module.status = "Prerequisite Not Met"
        
        context['module_list'] = course_modules
        return context
        

class StudentDashboardLessonView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    template_name = 'dashboard/student_lessons.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentDashboardLessonView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.get(slug=self.kwargs['module_slug'])
        
        module_lessons = Lesson.objects.filter(module__slug=self.kwargs['module_slug']).order_by('position')
        
        # Add dynamic fields to lessons
        for lesson in module_lessons:
            lesson.is_accessible = lesson.is_previous_lesson_done(self.request.user)
            try:
                progress = StudentLessonProgress.objects.get(student=self.request.user, lesson__slug=lesson.slug)
                lesson.done_percent = progress.done_percent
                lesson.status = progress.get_status_display()
            except StudentLessonProgress.DoesNotExist:
                lesson.done_percent = 0
                lesson.status = 'Not Started'
                
        context['lesson_list'] = module_lessons
        
        studentlessonprogress = StudentLessonProgress.objects.filter(student=self.request.user, lesson__module__slug=self.kwargs['module_slug'])
        
        context['lessons_progress'] = { progress.lesson.id: progress.done_percent for progress in studentlessonprogress }
        
        context['accessible_lesson_ids'] = studentlessonprogress.values_list('pk', flat=True)
        return context
        

class StudentDashboardLessonQuestionsView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    
    template_name = 'dashboard/questions_asked.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentDashboardLessonQuestionsView, self).get_context_data(**kwargs)
        context['student_lesson_questions'] = LessonQuestion.objects.filter(student=self.request.user).order_by('position')
        return context
        
        
class StudentLearnLessonView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    """
    View used for viewing/learning a specific lesson.
    """
    
    template_name = 'dashboard/learn_lesson.html'
    
    # required: Only users from Student group can access this view
    group_required = u"Student"
    
    def get_context_data(self, **kwargs):
        context = super(StudentLearnLessonView, self).get_context_data(**kwargs)
        
        lesson = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        context['lesson'] = lesson
        context['active_tab'] = "lesson"
        
        # Adding form for asking a question
        context['askquestion_form'] = AskQuestionForm(prefix='askquestion', initial={'sender': self.request.user, 'lesson':lesson})
                
        progress, created = StudentLessonProgress.objects.get_or_create(
                                                    student=self.request.user, 
                                                    lesson=lesson)
        if created:
            progress.status = IN_PROGRESS
            progress.done_percent += 10 # Incrementing percentage to 10
            progress.save()
            
        # Check if this lesson's question has been answered before
        exercises = lesson.get_exercises()
        if exercises:
            for exercise in exercises:
                
                # Get Questions if any
                context['questions'] = exercise.question_set.all()
                for question in exercise.question_set.all():
                    u_answers = UserAnswer.objects.filter(student=self.request.user, question=question)
                    context['answers'] = { u_answer  for u_answer in u_answers }

                # # Get Table Exercise Questions if any
                context['ta_questions'] = exercise.tableexercisequestion_set.all()
                for ta_question in exercise.tableexercisequestion_set.all():
                    ta_answers = TableExerciseUserAnswer.objects.filter(student=self.request.user, question=ta_question)
                    context['ta_answers'] = { ta_answer for ta_answer in ta_answers }
                    
                # Get Multichoice Questions if any
                context['multichoice_questions'] = exercise.multichoicequestion_set.all()
                for multichoice_question in exercise.multichoicequestion_set.all():
                    mc_answers = MultiChoiceUserSubmittedAnswer.objects.filter(student=self.request.user, question=multichoice_question)
                    context['mc_answers'] = { mc_answer  for mc_answer in mc_answers }
                    
                # Get Essay Questions if any
                context['essay_questions'] = exercise.essayquestion_set.all()
                for essay_question in exercise.essayquestion_set.all():
                    eq_answers = EssayUserAnswer.objects.filter(student=self.request.user, question=essay_question)
                    context['eq_answers'] = { eq_answer  for eq_answer in eq_answers }
        
        return context
        
    
class HowItWorksView(TemplateView):
    template_name = 'howitworks.html'
