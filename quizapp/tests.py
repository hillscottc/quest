from django.test import TestCase
from quizapp.models import Quiz


class QuizTestCase(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(name="testquiz")

    def test_quiz(self):
        print self.quiz1

