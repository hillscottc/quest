from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from quizapp.models import Question, Answer, Quiz
import os
import re
from ...utils import FILE_BASE_DIR

from os import walk

FILES = []
for (dirpath, dirnames, filenames) in walk(FILE_BASE_DIR):
    FILES.extend(filenames)
    break


class Command(BaseCommand):
    args = ''
    help = 'Parse quizball files.'

    def handle(self, *args, **options):
        for f in FILES:

            soup = BeautifulSoup(open(os.path.join(FILE_BASE_DIR, f)))

            quiz = Quiz.objects.create(source="QUIZBALLS",
                                       name="Sample Quiz %s" % re.search(r'\d+', f).group())

            for (i, td) in enumerate(soup.find_all('td', {"width": "350"})):
                Question.objects.create(quiz=quiz, text=td.get_text(),
                                        order=i, ans_type=Question.FILLIN)

            for (i, td) in enumerate(soup.find_all('td', {"valign": "bottom"})):
                question = Question.objects.get(quiz=quiz, order=i)
                Answer.objects.create(question=question, text=td.get_text(), correct=True)

            self.stdout.write("\nCreated quiz %s with %d questions and %d answers." % (
                quiz,
                quiz.questions.count(),
                Answer.objects.filter(question__in=Question.objects.filter(quiz=quiz)).count()))


