from quizapp.models import RawLog, QuizLog


# def raw_log(message, taker=None, owner=None):
#     if taker:
#         message = "%s %s" % (taker, message)
#
#     RawLog.objects.create(message=message)


def log_message(quiz, taker, message):
    RawLog.objects.create(message="%s %s %s" % (taker, message, quiz))
    # QuizLog.objects.create(**locals())

