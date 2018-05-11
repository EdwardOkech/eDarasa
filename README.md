python manage.py loaddata initial_data_for_groups.json

python manage.py dumpdata exercises.multichoiceuseranswer --indent=4 > module_options.json --settings=jm_lms.settings.prod

fab prod restart

fab prod deploy

USING THE SHELL
================
python manage.py shell --settings=jm_lms.settings.prod
e.g.
>>> from jm_lms.apps.quiz.models import Quiz
>>> from jm_lms.apps.courses.models import Lesson



