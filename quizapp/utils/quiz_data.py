"""Model data for loading."""
from quizapp.models import Question, Answer


def add_questions(quiz):
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


# def qset2(quiz):
#     q = Question.objects.create(text="How many sides on a triangle?", quiz=quiz)
#     Answer.objects.create(question=q, text="3", correct=True)
#     Answer.objects.create(question=q, text="4")
#     Answer.objects.create(question=q, text="5")
#
#     q = Question.objects.create(text="What is the name of the official national anthem of the USA?", quiz=quiz)
#     Answer.objects.create(question=q, text="The Star-Spangled Banner", correct=True)
#     Answer.objects.create(question=q, text="America the Beautiful")
#     Answer.objects.create(question=q, text="Stars and Stripes Forever")
#
#     q = Question.objects.create(text="What is the capital city of Afghanistan?", quiz=quiz)
#     Answer.objects.create(question=q, text="Kabul", correct=True)
#     Answer.objects.create(question=q, text="Falujah")
#     Answer.objects.create(question=q, text="Darfur")
#
#     q = Question.objects.create(text="Which two colours are on the flag of Poland?", quiz=quiz)
#     Answer.objects.create(question=q, text="Red and White", correct=True)
#     Answer.objects.create(question=q, text="Red and Blue")
#     Answer.objects.create(question=q, text="Red and Green")


# def qset3(quiz):
#     q = Question.objects.create(text="How many US states begin with the letter 'P'", quiz=quiz)
#     Answer.objects.create(question=q, text="1", correct=True)
#     Answer.objects.create(question=q, text="2")
#     Answer.objects.create(question=q, text="3")
#
#     q = Question.objects.create(text="Paraguay has borders with Brazil, Bolivia and which other country?", quiz=quiz)
#     Answer.objects.create(question=q, text="Argentina", correct=True)
#     Answer.objects.create(question=q, text="Venezuela")
#     Answer.objects.create(question=q, text="Belize")
#
#     q = Question.objects.create(text="In which country is Mount Everest?", quiz=quiz)
#     Answer.objects.create(question=q, text="Nepal", correct=True)
#     Answer.objects.create(question=q, text="China")
#     Answer.objects.create(question=q, text="India")
#
#     q = Question.objects.create(text="What is the national currency of Egypt?", quiz=quiz)
#     Answer.objects.create(question=q, text="The Lira")
#     Answer.objects.create(question=q, text="The Dollar")
#     Answer.objects.create(question=q, text="The Pound", correct=True)


