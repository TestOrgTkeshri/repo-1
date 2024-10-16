import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_models.tests.settings"

    django.setup()

    test_folder = []
    if len(sys.argv) > 1:
        test_folder.append(sys.argv[1])

    test_runner = get_runner(settings)
    failures = test_runner().run_tests(test_folder)
    sys.exit(bool(failures))
