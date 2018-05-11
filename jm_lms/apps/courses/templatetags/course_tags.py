from django import template
from jm_lms.apps.courses.models import Module, Lesson
#from django.db.models.query import RawQuerySet

def do_module_last_lesson(parser, token):
    return ModuleLastLessonNode()


class ModuleLastLessonNode(template.Node):


    def render(self, context):
        # # a = [i[-1] for i in StudentLessonProgress.objects.filter(status=2)]
        # if StudentLessonProgress.objects.filter(status=2) and Lesson.module.
        # last_lesson = Module.get_student_progress_in_module(last_lesson_in_module)
        # context['completed_module'] = StudentLessonProgress.objects.filter(status=2)
        # context['last_lesson'] = Lesson.objects.raw(
        #     "select max(id) from courses_lesson where module_id in (select module_id from courses_lesson group by module_id having count (*) > 1)"
        #   )
        # context['last_lesson_mod'] = Module.get_last_lesson_in_module()
        lessons = Lesson.objects.all()
        lessons_in_module = lessons.select_related('module')
        context['last_lesson'] = lessons_in_module.order_by('-position')[0]

        return ''

register = template.Library()
register.tag('get_module_last_lesson', do_module_last_lesson)

# register = template.Library()

# @register.simple_tag
# def module_last_lesson(module):
#     module = Module.objects.get(pk=module.pk)
#     module_lessons = module.lesson_set.all()
#     last_lesson = module_lessons.order_by('-position')[0]
#     return last_lesson
