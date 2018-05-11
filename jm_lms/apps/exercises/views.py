from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

from jm_lms.apps.courses.models import Course, Module, Lesson, StudentLessonProgress, IN_PROGRESS, COMPLETED
from jm_lms.apps.exercises.models import Exercise, ExerciseSubmission, Question, UserAnswer, MultiChoiceQuestion, MultiChoiceQuestionOption, MultiChoiceUserSubmittedAnswer, EssayQuestion, EssayUserAnswer
from .models import TableExerciseQuestion, TableExerciseUserAnswer

def lesson_exercise_posted(request, lesson_id, exercise_id):
    
    lesson = Lesson.objects.get(pk=lesson_id)
    exercise = Exercise.objects.get(pk=exercise_id)
    exercise_submission, created = ExerciseSubmission.objects.get_or_create(
                                             student=request.user,
                                             #lesson=lesson,
                                             exercise=exercise)
                                             
    if created:    
        for key in request.POST.iterkeys():
            value = request.POST.get(key)
            print("{0}:::{1}".format(key, value))
            
            if value:        
                # Get List Questions; Can be more than one
                if key.startswith('qu'):            
                    prefix, question_id, question_counter = key.split('-')
                    qu_question = Question.objects.get(pk=question_id)
                    user_answer = UserAnswer(student=request.user, 
                                             question=qu_question,
                                             answer=value.strip(),
                                             exercise_submission=exercise_submission)
                    user_answer.save()

                # Get table exercise questions
                if key.startswith('ta'):
                    prefix, question_id, question_counter = key.split('-')
                    ta_question = TableExerciseQuestion.objects.get(pk=question_id)
                    table_answer = TableExerciseUserAnswer(student=request.user,
                                                           question=ta_question,
                                                           answer=value.strip(),
                                                           exercise_submission=exercise_submission)
                    table_answer.save()
                    
                # Get Multichoice Questions
                if key.startswith('mcq'):
                    prefix, question_id, choice_counter = key.split('-')
                    mc_question = MultiChoiceQuestion.objects.get(pk=question_id)
                    mc_option_selected = MultiChoiceQuestionOption.objects.get(question=mc_question, content=value.strip())
                    mc_answer = MultiChoiceUserSubmittedAnswer(
                                                student=request.user, 
                                                question=mc_question, 
                                                selected_choice=mc_option_selected,
                                                exercise_submission=exercise_submission)
                    mc_answer.save()
            
                # Get Essay Questions
                if key.startswith('eq'):
                    prefix, question_id = key.split('-')
                    essay_question = EssayQuestion.objects.get(pk=question_id)               
                    try:
                        essay_answer = EssayUserAnswer.objects.get(student=request.user, question=essay_question)
                    except EssayUserAnswer.DoesNotExist:
                        essay_answer = EssayUserAnswer(student=request.user, 
                                             question=essay_question,
                                             answer=value.strip(),
                                             exercise_submission=exercise_submission)
                        essay_answer.save()
                        
        # Update the user progress
        progress = StudentLessonProgress.objects.get(student=request.user, lesson=lesson)
        progress.status = COMPLETED
        progress.done_percent = 100 # Incrementing percentage at this stage to make it 100
        progress.save()
        # if progress.done_percent == 100:
        #     messages.info(request,"Congratulations! you have finished this module")
        
        messages.success(request, "Thank you! Your answer submission has been saved. Click on the Answers tab to reveal the correct answers.")
    else:
        messages.success(request, "Thank you! Your answer submission was NOT saved because you had previously done this exercise.")
        
    return HttpResponseRedirect( '{0}#answers'.format(reverse('learn_lesson', 
                                kwargs={
                                'course_slug':lesson.module.course.slug,
                                'module_slug':lesson.module.slug,
                                'lesson_slug':lesson.slug}
                                )))
