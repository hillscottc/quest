import os
from random import randint
import re
import logging
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
import requests
from requests import ConnectionError, HTTPError
from quizapp.models import Quiz, Question, Answer

log = logging.getLogger(__name__)


def load_all():
    src_files = []
    for (dirpath, dirnames, filenames) in os.walk(settings.QUIZ_SCRAPE_DIR):
        src_files.extend(filenames)
        break

    created = []

    for f in src_files:

        soup = BeautifulSoup(open(os.path.join(settings.QUIZ_SCRAPE_DIR, f)))

        quiz = Quiz.objects.create(source="QUIZBALLS",
                                   name="Sample Quiz %s" % re.search(r'\d+', f).group())

        created.append(quiz)

        for (i, td) in enumerate(soup.find_all('td', {"width": "350"})):
            Question.objects.create(quiz=quiz, text=td.get_text(),
                                    order=i, ans_type=Question.FILLIN)

        for (i, td) in enumerate(soup.find_all('td', {"valign": "bottom"})):
            question = Question.objects.get(quiz=quiz, order=i)
            Answer.objects.create(question=question, text=td.get_text(), correct=True)

        log.debug("Created quiz %s with %d questions and %d answers." % (
            quiz,
            quiz.questions.count(),
            Answer.objects.filter(question__in=Question.objects.filter(quiz=quiz)).count()))
    log.info("Loaded %s quizzes." % len(created))
    return created


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


def scrape_all():
    for url in QB_URLS.keys():
        for quiz_id in QB_URLS[url]:
            url = url.format(quiz_id)
            filename_template = "{}.html"
            outfile = os.path.join(settings.QUIZ_SCRAPE_DIR,
                                   filename_template.format(quiz_id))

            print("\nGET: %s" % url)
            try:
                r = requests.get(url)
                # self.stdout.write("Length of content %d, status %s" % (len(r.content), r.status_code))
                if r.status_code != requests.codes.ok:
                    raise ConnectionError("FAIL: %s %s" % (r.status_code, url))
            except (ConnectionError, HTTPError), e:
                print str(e)
                continue

            with open(outfile, "wb") as f:
                f.write(r.content)
            print("WROTE: %s" % outfile)


QB_URLS = {
    "http://quizballs.com/quiz-{}-general-knowledge-qa  /print/": [
        1025, 1026, 1027, 1028, 1029, 1030, 1034, 1039, 1042, 1043, 1045, 1046, 1048, 1049, 1051,
        1052, 1053, 1054, 1056, 1057, 1059, 1060, 1062, 1063, 1065, 1067, 1068, 1069, 1070,
    ],
    "http://quizballs.com/quiz-1031-general-knowledge-qa-2/print/": [
        1032, 1033, 1037, 1038, 1047, 1064,
    ],
    "http://quizballs.com/quiz-{}-general-knowledge/print/": [
        1035, 1039, 1040, 1050,
    ],
    "http://quizballs.com/quiz-{}-with-answers/print/": [
        1021, 1022, 1023, 1024
    ],
}


