from django.conf import settings
from django.db import models
#from django.db.models import get_model
from django.utils.translation import ugettext as _


#from jm_lms.apps.courses.models import Module # This is causing cyclic importation
#import django
#django.setup()


class Exercise(models.Model):
    title = models.CharField(max_length=256, null=True)
    
    def __unicode__(self):
        return self.title
        

class ExerciseSubmission(models.Model):
    """ Data Model representing a student's exercise Submission. """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Student', related_name='exercise_submissions')
    exercise = models.ForeignKey(Exercise, verbose_name=_("Exercise"))
    #lesson = get_model('jm_lms.apps.courses.models', 'Lesson') #models.ForeignKey(Lesson, verbose_name='Lesson')
    date = models.DateTimeField(editable=False, auto_now_add=True)
    
    class Meta:
        verbose_name = _("Exercise Submission")
        verbose_name_plural = _("Exercise Submissions")


class BaseQuestion(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name=_("Exercise"))
    title = models.TextField(verbose_name=_("Topic Box"), blank=True, null=True, help_text=_("Exercise Topic Title and description"))
    expected_answer = models.TextField(verbose_name="Expected Answer", blank=True, null=True, help_text=_("How the learner should answer the question. Shown after the question has been answered."))
    # the two preceding fields enable question answers to be forwarded to other exercises
    forward = models.BooleanField(default=False, verbose_name=_("Forward Answer?"), help_text=_("Click to forward user's answer to another exercise"))

    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title


class Question(BaseQuestion):
    num_of_expected_answers = models.IntegerField(default=1, verbose_name=_("Number of expected answers"))
    forward_to_exercise = models.ManyToManyField(Exercise, verbose_name=_("Forward To Exercise"), blank=True,
                                                 related_name='forwarded_exercises_answers')
    
    class Meta:
        verbose_name = _("List Question")
        verbose_name_plural = _("List Questions")
    



class UserAnswer(models.Model):
    """
    Response given by a user
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Student', related_name='exercise_answers')
    question = models.ForeignKey(Question, verbose_name=_("Question"))
    answer = models.CharField(max_length=256, null=True)
    answered_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    exercise_submission = models.ForeignKey(ExerciseSubmission, verbose_name=_("Exercise Submission"), blank=True, null=True)


    class Meta:
        ordering = ("id",)
        verbose_name = _("User Answer to List Question")
        verbose_name_plural = _("User Answers to List Question")
        
    def __unicode__(self):
        return self.answer
        
        
class MultiChoiceQuestion(BaseQuestion):
    forward_to_exercise = models.ManyToManyField(Exercise, verbose_name=_("Forward To Exercise"), blank=True,
                                                 related_name='forwarded_exercises_answers_mc')
    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")
        
    def check_if_correct(self, guess):
        answer = MultiChoiceQuestionOption.objects.get(id=guess)

        if answer.correct is True:
            return True
        else:
            return False
            
    def get_answers(self):
        return MultiChoiceQuestionOption.objects.filter(question=self)

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in MultiChoiceQuestionOption.objects.filter(question=self)]
        
        
class MultiChoiceQuestionOption(models.Model):
    question = models.ForeignKey(MultiChoiceQuestion, verbose_name=_("Question"))
    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that you want displayed"),
                               verbose_name=_("Answer Content"))
    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))
                                      
    class Meta:
        verbose_name = _("MultiChoice Option")
        verbose_name_plural = _("MultiChoice Options")
        
    def __unicode__(self):
        return self.content
        
        
class MultiChoiceUserSubmittedAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Student', related_name='exercise_submitted_choice')
    question = models.ForeignKey(MultiChoiceQuestion, verbose_name=_("Question"))
    selected_choice = models.ForeignKey(MultiChoiceQuestionOption, verbose_name=_("Question"))
    answered_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    exercise_submission = models.ForeignKey(ExerciseSubmission, verbose_name=_("Exercise Submission"), blank=True, null=True)

    
    class Meta:
        verbose_name = _("MultiChoice Submitted User Answer")
        verbose_name_plural = _("MultiChoice Submitted User Answers")
        
    def __unicode__(self):
        return self.selected_choice.content

        
class EssayQuestion(BaseQuestion):
    forward_to_exercise = models.ManyToManyField(Exercise, verbose_name=_("Forward To Exercise"), blank=True,
                                                 related_name='forwarded_exercises_answers_eq')
    class Meta:
        verbose_name = _("Essay Question")
        verbose_name_plural = _("Essay Questions")

       
class EssayUserAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Student', related_name='exercise_essay_answers')
    question = models.ForeignKey(EssayQuestion, verbose_name=_("Question"))
    answer = models.TextField(null=True, blank=True)
    answered_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    exercise_submission = models.ForeignKey(ExerciseSubmission, verbose_name=_("Exercise Submission"), blank=True, null=True)


class TableExerciseQuestion(BaseQuestion):
    table_header = models.CharField(max_length=256, null=True)
    num_of_expected_entries = models.IntegerField(default=1, verbose_name=_("Number of expected entries"))
    forward_to_exercise = models.ManyToManyField(Exercise, verbose_name=_("Forward To Exercise"), blank=True,
                                                 related_name='forwarded_exercises_answers_ta')

    class Meta:
        verbose_name = _("Table Exercise Question")
        verbose_name_plural = _("Table Exercise Questions")

    def __unicode__(self):
        return self.table_header


class TableExerciseUserAnswer(models.Model):
    """
    Response given by a user
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The Student', related_name='table_exercise_answers')
    question = models.ForeignKey(TableExerciseQuestion, verbose_name=_(" Table Exercise Question"))
    answer = models.CharField(max_length=256, null=True)
    answered_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    exercise_submission = models.ForeignKey(ExerciseSubmission, verbose_name=_("Exercise Submission"), blank=True, null=True)

    class Meta:
        ordering = ("id",)
        verbose_name = _("User Answer to Table Exercise Question")
        verbose_name_plural = _("User Answers to Table Exercise Question")

    def __unicode__(self):
        return self.answer







