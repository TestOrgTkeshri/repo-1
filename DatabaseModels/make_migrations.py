import os

import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_models.tests.settings"

    django.setup()

    execute_from_command_line(["make_migrations.py", "makemigrations"])
