"""Gets html pages from Quizballs, saves to local dir.
"""
from django.core.management.base import BaseCommand
import requests
from requests.exceptions import ConnectionError, HTTPError
import os
from django.conf import settings

QB_URLS = {
    "http://quizballs.com/quiz-{}-general-knowledge-qa/print/": [
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


class Command(BaseCommand):
    args = ''
    help = 'Download quizball pages.'

    def handle(self, *args, **options):
        """Gets html pages from Quizballs, saves to local dir.
        """

        for url in QB_URLS.keys():
            for quiz_id in QB_URLS[url]:
                url = url.format(quiz_id)
                filename_template = "{}.html"
                outfile = os.path.join(settings.QUIZ_SCRAPE_DIR,
                                       filename_template.format(quiz_id))

                self.stdout.write("\nGET: %s" % url)
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
                self.stdout.write("WROTE: %s" % outfile)

