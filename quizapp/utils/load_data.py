"""Model data for loading."""
from quizapp.models import Quiz, Question, Answer
from django.contrib.auth.models import User
from random import randint
from quiz_data import add_questions


def get_or_create_profile():
    """get-or-create test profile model data."""
    teacher, _ = User.objects.get_or_create(username='Teacher1')
    # org, _ = Organization.objects.get_or_create(name="School1")
    # clsrm, _ = Classroom.objects.get_or_create(organization=org, name="Class1")
    # return tuple(teacher, org, clsrm)
    return teacher


def create_sample_quiz():
    # teacher, org, clsrm = get_or_create_profile()
    teacher = get_or_create_profile()

    quiz = Quiz.objects.create(owner=teacher,
                               name="Sample Quiz %s" % randint(1, 1000))
    q = Question.objects.create(text="What is the name of the first US president?", quiz=quiz)
    Answer.objects.create(question=q, text="Lincoln")
    Answer.objects.create(question=q, text="Kennedy")
    Answer.objects.create(question=q, text="Washington", correct=True)

    q = Question.objects.create(text="How many planets are in our solar system?", quiz=quiz)
    Answer.objects.create(question=q, text="7")
    Answer.objects.create(question=q, text="8", correct=True)
    Answer.objects.create(question=q, text="9")

    q = Question.objects.create(text="What is the fourth planet from the sun?", quiz=quiz,
                                ans_type="UL")
    Answer.objects.create(question=q, text="Mars", correct=True)
    print "Created quiz", quiz


