import logging

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from positions.fields import PositionField

from jm_lms.apps.exercises.models import Exercise
from jm_lms.apps.quiz.models import Quiz



log = logging.getLogger(__name__)


NOT_STARTED = 0
IN_PROGRESS = 1
COMPLETED = 2
PROGRESS_STATUS = (
    (NOT_STARTED, _("Not Started")),
    (IN_PROGRESS, _("In Progress")),
    (COMPLETED, _("Completed"))
)


class Course(models.Model):
    """
    Data model representing a course.
    A course can have one or more modules.
    """
    name = models.CharField(verbose_name=_("Course Name"), max_length=200, help_text=_('The course title'))
    description = models.TextField(verbose_name="Course Description", help_text=_("Course description"))
    prerequisite = models.ForeignKey('self', verbose_name=_("Prerequisite Course"), null=True, blank=True, default=None)   
    slug = models.SlugField(editable=False, help_text=_('Unique identifier'))
    position = PositionField(collection='prerequisite')
    position_order = models.IntegerField(verbose_name=_("Order to be shown in views"), default=0)
    
    class Meta:
        verbose_name_plural = "Courses"
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('course_detail', args=[self.slug])
        
    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.name)
            new_slug = slug
            count = 0
            while Course.objects.filter(slug=new_slug).exclude(id=self.id).count() > 0:
                count += 1
                new_slug = '{slug}-{count}'.format(slug=slug, count=count)
            self.slug = new_slug
            
        super(Course, self).save(*args, **kwargs)
        
    @property    
    def previous_course(self):
        if self.prerequisite is None:
            return Course.objects.None()
        return self.prerequisite
        
    def _student_count(self):
        raise NotImplementedError
        
    @classmethod
    def get_student_progress_in_course(cls, student, course):
        """
        Calculates the progress of the given student in a particular course.
        This is achieved by summing up the module progress of the student.
        """
        progress = 0
        try:
            course = Course.objects.get(pk=course.pk)
            course_modules = course.module_set.all()
            num_of_modules_in_course = course_modules.count()
            
            # Current progress of all the modules done by a student
            curr_module_progress_total = 0
            for module in course_modules:
                curr_module_progress_total += Module.get_student_progress_in_module(student, module)
                
            # Calculate current course progress of the student
            progress = (100*curr_module_progress_total)/(num_of_modules_in_course*100)
        except ZeroDivisionError:
            progress = 0
        return progress
        
    @property    
    def has_previous_course(self):
        if self.prerequisite:
            return True
        return False
        
    def is_previous_course_done(self, student):
        """
        Determine if a previous course has been completed by student.
        """
        if not self.has_previous_course:
            return True
        elif self.has_previous_course:
            try:
                total_course_score = StudentLessonProgress.objects.filter(student=student, lesson__module__course=self.prerequisite).aggregate(total_percentage=Sum('done_percent'))
                course_score_result = total_course_score.get('total_percentage', 0)
                
                student_course_progress = (course_score_result*100) / (self.prerequisite.module_set.all().count()*100)
                
                if student_course_progress >= 100:
                    return True
            except (StudentLessonProgress.DoesNotExist, ZeroDivisionError, TypeError):
                return False            
        return False
    

class Module(models.Model):
    DRAFT = 1
    SUSPENDED = 2
    PUBLISHED = 3
    MODULE_STATUSES = (
        (DRAFT, _("Draft")),
        (SUSPENDED, _("Suspended")),
        (PUBLISHED, _("Published"))
    )
    course = models.ForeignKey(Course)
    name = models.CharField(verbose_name=_("Module Name"), max_length=200, help_text=_('The module title'))
    description = models.TextField(verbose_name="Module Description", help_text=_("Module description"))
    prerequisite = models.ForeignKey('self', verbose_name=_("Prerequisite Module"), null=True, blank=True, default=None)   
    slug = models.SlugField(editable=False, help_text=_('Unique identifier'))
    status = models.IntegerField(verbose_name="Module Status", choices=MODULE_STATUSES, default=PUBLISHED)
    position = PositionField(collection='course', default=0)
    end_of_module = models.TextField(verbose_name=_("Module Summary"), default=None, null=True, help_text=_("Wrap and summarize this module"))
    last_module = models.ForeignKey('self', verbose_name=_("Previous Module"), null=True, blank=True, default=None, related_name="previous_module")
    next_module = models.ForeignKey('self', verbose_name=_("Next Module"), null=True, blank=True, default=None, related_name="the_next_module")
    

    class Meta:
        verbose_name_plural = "Modules"
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('module_detail', args=[self.slug])
        
    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.name)
            new_slug = slug
            count = 0
            while Module.objects.filter(slug=new_slug).exclude(id=self.id).count() > 0:
                count += 1
                new_slug = '{slug}-{count}'.format(slug=slug, count=count)
            self.slug = new_slug           
            
        super(Module, self).save(*args, **kwargs)
        
    @classmethod
    def get_student_progress_in_module(cls, student, module):
        """
        Calculates the progress of the given student in a particular module.
        This is achieved by summing up the lesson progress of the student.
        """
        progress = 0
        try:
            if module:
                module = Module.objects.get(pk=module.pk)
                module_lessons = module.lesson_set.all()
                num_of_lessons_in_module = module_lessons.count()
                # last_lesson_in_module = [index for index, item in enumerate(module_lessons)[len(module_lessons)-1::]]
                # a = module_lessons.order_by('id')
                # b = list(a.values_list('id', flat=True)).index(obj.id)
                # last_lesson = b[len(b)-1::]

                # Current progress of all the lessons done by a student
                curr_lesson_progress_total = 0
                for lesson in module_lessons:
                    curr_lesson_progress_total += Lesson.get_student_progress_in_lesson(student, lesson)

                # Calculate current module progress of the student
                progress = (100*curr_lesson_progress_total)/(num_of_lessons_in_module*100)
        except ZeroDivisionError, AttributeError:
            progress = 0
        return progress

    # @classmethod
    # def get_last_lesson_in_module(cls, student, module):
    #     last_lesson = Module.objects.raw(
    #         "select * from courses_lesson where module_id in (select module_id from courses_lesson group by module_idhaving count (*) > 1)"
    #      )
    #
    #     # if module:
    #     #     module = Module.objects.get(pk=module.pk)
    #     #     module_lessons = module.lesson_set.all()
    #     #     last_lesson_in_module = module_lessons[-1]
    #     return last_lesson

        
    @property    
    def has_previous_module(self):
        if self.prerequisite:
            return True
        return False

        
    def is_previous_module_done(self, student):
        """
        Determine if a previous module has been completed by student.
        """
        if not self.has_previous_module:
            return True
        elif self.has_previous_module:
            try:
                total_module_score = StudentLessonProgress.objects.filter(student=student, lesson__module=self.prerequisite).aggregate(total_percentage=Sum('done_percent'))
                module_score_result = total_module_score.get('total_percentage', 0)
                
                student_module_progress = (module_score_result*100) / (self.prerequisite.lesson_set.all().count()*100)
                
                if student_module_progress >= 100:
                    return True
            except (StudentLessonProgress.DoesNotExist, ZeroDivisionError, TypeError):
                return False            
        return False
        




class Lesson(models.Model):
    module = models.ForeignKey(Module)
    name = models.CharField(verbose_name=_("Lesson Title"), max_length=200, help_text=_('The lesson title'))
    prerequisite = models.ForeignKey('self', verbose_name=_("Prerequisite Lesson"), null=True, blank=True, default=None)   
    content = models.TextField()
    instructions_before = models.TextField(verbose_name=_("Instructions before exercise"), null=True, blank=True, default=None)
    instructions_after = models.TextField(verbose_name=_("Instructions after exercise"), null=True, blank=True, default=None)
    quizzes = models.ManyToManyField(Quiz, verbose_name=_("Quiz"), blank=True, related_name='lessons')
    slug = models.SlugField(editable=False, help_text=_('Unique identifier'))
    exercises = models.ManyToManyField(Exercise, verbose_name=_("Exercise"), blank=True, related_name='lesson_exercises')
    position = PositionField(collection='module', default=0)
        
    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
    
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('lesson_detail', args=[self.slug])
        
    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.name)
            new_slug = slug
            count = 0
            while Lesson.objects.filter(slug=new_slug).exclude(id=self.id).count() > 0:
                count += 1
                new_slug = '{slug}-{count}'.format(slug=slug, count=count)
            self.slug = new_slug           
            
        super(Lesson, self).save(*args, **kwargs)
        
    @property
    def course(self):
        return self.module.course
    
    @property    
    def next_lesson(self):
        return Lesson.objects.get(prerequisite__id=self.id)
    
    @property    
    def has_previous_lesson(self):
        if self.prerequisite:
            return True
        return False
        
    @property    
    def previous_lesson(self):
        if self.prerequisite is None:
            return Lesson.objects.none()        
        return self.prerequisite

        
    def is_previous_lesson_done(self, student):
        """
        Determine if a previous lesson has been completed by student.
        """
        if not self.has_previous_lesson:
            return True
        elif self.has_previous_lesson:
            try:
                student_lesson_progress = StudentLessonProgress.objects.get(student=student, lesson=self.prerequisite)
                print(student_lesson_progress.done_percent)
                if student_lesson_progress.done_percent >= 100:
                    return True
            except StudentLessonProgress.DoesNotExist:
                return False            
        return False
        
    @classmethod
    def get_student_progress_in_lesson(cls, student, lesson):		
		progress = 0
		try:
		    student_lesson_progress = StudentLessonProgress.objects.get(student=student, lesson=lesson)
		    progress = student_lesson_progress.done_percent 
		except (StudentLessonProgress.DoesNotExist):
		    progress = 0
		return progress
        
    def get_quizzes(self):
        return self.quizzes.all()
        
    def get_exercises(self):
        return self.exercises.all()
        
        
class LessonQuestion(models.Model):
    """
    Represents a Student's question in regards to a given lesson
    """
    CLOSED = 0
    OPEN = 1
    QUESTION_STATUSES = (
        (CLOSED, _("Closed")),
        (OPEN, _("Open"))
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The asker of the question', related_name='student_lesson_questions')
    lesson = models.ForeignKey(Lesson, verbose_name='Lesson', help_text=_("The Lesson to get more information about."))
    title = models.CharField(verbose_name=_("Question Title"), max_length = 200)
    description = models.TextField(verbose_name="Student Question Description", help_text=_("Description about the question"))
    date_asked = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    status = models.IntegerField(verbose_name="Question Status", choices=QUESTION_STATUSES, default=OPEN)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = _("Lesson Question")
        verbose_name_plural = _("Lesson Questions")
        

class LessonQuestionResponse(models.Model):
    """
    Represents an answer to a Student's question in regards to a given lesson
    """
    lesson_question = models.ForeignKey(LessonQuestion, verbose_name='Lesson Question')
    replier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The replier to the question')
    reply = models.TextField(verbose_name="Reply to Student Question", help_text=_("Answer to Student Question"))
    date_answered = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    
    class Meta:
        ordering = ['-date_answered']
        verbose_name = _("Response to Lesson Question")
        verbose_name_plural = _("Response to Lesson Questions")
        

class Example(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    link = models.URLField(blank = True)
    file = models.FileField(upload_to = 'examples_upload/%Y/%m/%d', blank = True)

    class Meta:
        verbose_name = _("Example")
        verbose_name_plural = _("Examples")
        
    def __unicode__(self):
        return self.title
        

class CourseEnrollmentException(Exception):
    pass
    
    
class AlreadyEnrolledError(CourseEnrollmentException):
    pass
    
    
class CourseEnrollmentManager(models.Manager):
    """
    Custom manager for CourseEnrollment.
    """

    def num_enrolled_in(self, course):
        """
        Returns the count of active enrollments in a course.
        """
        enrollment_number = super(CourseEnrollmentManager, self).get_query_set().filter(
            course=course,
            is_active=1
        ).count()
        return enrollment_number
        
    def users_enrolled_in(self, course):
        """Return a queryset of User for every user enrolled in the course."""
        return User.objects.filter(
            courseenrollment__course=course,
            courseenrollment__is_active=True
        )
    
    
class CourseEnrollment(models.Model):
    """
    Represents a Student's Enrollment record for a single Course.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Enrolled', related_name='enrolment_student',
                                help_text=_("Enrol this user as student in Course."))
    course = models.ForeignKey(Course, verbose_name='In Course', help_text=_("Course of Enrolment."))
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    
    # If is_active is False, then the student is not considered to be enrolled in the course (is_enrolled() will return False)
    is_active = models.BooleanField(default=True)
    
    objects = CourseEnrollmentManager()
    
    class Meta(object):
        unique_together = (('student', 'course'),)
        ordering = ('student', 'course')
        
    def __unicode__(self):
        return ("[CourseEnrollment] {}: {} ({}); active: ({})"
        ).format(self.student, self.course, self.created, self.is_active)
        
    @classmethod
    def is_enrolled(cls, student, course):
        """
        Returns True if the user is enrolled in the course (the entry must exist
        and it must have `is_active=True`). Otherwise, returns False.
        'student' is a Django User object. If it hasn't been saved yet (no `.id`
               attribute), this method will automatically save it before
               adding an enrollment for it.
        'course' is our usual course object
        """
        try:
            record = CourseEnrollment.objects.get(student=student, course=course)
            return record.is_active
        except cls.DoesNotExist:
            return False
            
    @classmethod
    def get_or_create_enrollment(cls, student, course):
        """
        Create an enrollment for a user in a class. By default *this enrollment
        is not active*. This is useful for when an enrollment needs to go
        through some sort of approval process before being activated. If you
        don't need this functionality, just call 'enroll()' instead.
        """
        enrollment, created = CourseEnrollment.objects.get_or_create(
            student=student,
            course=course,
        )
        
         # If we *did* just create a new enrollment, set some defaults
        if created:
            enrollment.is_active = False
            enrollment.save()

        return enrollment
        
    def update_enrollment(self, is_active=None):
        """
        Updates an enrollment for a user in a class.
        This saves immediately.
        """
        if self.is_active != is_active and is_active is not None:
            self.is_active = is_active
            self.save()
        
    @classmethod
    def enroll(cls, student, course):
        """
        Enroll a student in a course. This saves immediately.
        """
        if CourseEnrollment.is_enrolled(student, course):
            log.warning(
                u"User %s attempted to enroll in %s, but they were already enrolled",
                student.username,
                course.name
            )
            raise AlreadyEnrolledError
        
        # User is allowed to enroll if they've reached this point.
        enrollment = cls.get_or_create_enrollment(student, course)
        enrollment.update_enrollment(is_active=True)
        return enrollment
        
    @classmethod
    def unenroll(cls, student, course):
        """
        Remove the student from a given course. If the relevant `CourseEnrollment`
        object doesn't exist, we log an error but don't throw an exception.
        """
        try:
            record = CourseEnrollment.objects.get(student=student, course=course)
            record.update_enrollment(is_active=False)

        except cls.DoesNotExist:
            log.error(
                u"Tried to unenroll student %s from %s but they were not enrolled",
                student,
                course
            )
            
    def activate(self):
        """Makes this 'CourseEnrollment' record active. Saves immediately."""
        self.update_enrollment(is_active=True)

    def deactivate(self):
        """Makes this 'CourseEnrollment' record inactive. Saves immediately. An
        inactive record means that the student is not enrolled in this course.
        """
        self.update_enrollment(is_active=False)
        
        
class StudentLessonProgressManager(models.Manager):

    def get_student_current_lesson(self, student):
        try:
            progress = self.filter(student=student).latest('modified')
            if progress:
                return progress.lesson
        except StudentLessonProgress.DoesNotExist:
            return None        
        return None
        
    def get_student_current_module(self, student):
        lesson = self.get_student_current_lesson(student)
        if lesson:
            return lesson.module
        return None
        
    def get_student_current_course(self, student):
        module = self.get_student_current_module(student)
        if module:
            return module.course
        return None


class StudentLessonProgress(models.Model):
    """
    Holds all lesson state for a given user.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    lesson = models.ForeignKey(Lesson)
    status = models.IntegerField(verbose_name="Lesson Status", choices=PROGRESS_STATUS, default=NOT_STARTED)
    done_percent = models.IntegerField(default=0)
    
    # The following two fields can be used to calculate how long it took a 
    # student to complete a lesson.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = StudentLessonProgressManager()
    
    class Meta:
        verbose_name = "Student Lesson Progress"
        unique_together = (("student", "lesson"),)

