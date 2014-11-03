from django.shortcuts import render



def log_view(request):
    """The log page."""
    # all_log = RawLog.objects.all().order_by('-created_at')[:50]
    #
    # if request.user.is_authenticated():
    #     my_quiz_log = QuizSession.objects.filter(
    #         taker=request.user).order_by('-updated_at')[:50]
    # else:
    #     my_quiz_log = None

    return render(request, 'log.html',
                  # {'all_log': all_log, 'my_quiz_log': my_quiz_log},
                  # context_instance=RequestContext(request, processors=[custom_context_proc])
                  )


__all__ = [
    'log_view',
]