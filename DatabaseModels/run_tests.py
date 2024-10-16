import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_models.tests.settings"

    django.setup()

    test_runner = get_runner(settings)
    failures = test_runner().run_tests(["django_models"])
    sys.exit(bool(failures))
