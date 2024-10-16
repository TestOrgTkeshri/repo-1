import atexit
from urllib.parse import urlparse

import testing.postgresql

INSTALLED_APPS = [
    'django_models'
]

postgresql = testing.postgresql.Postgresql()
database_details = urlparse(postgresql.url())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test",
        "USER": database_details.username,
        "PASSWORD": database_details.password,
        "HOST": database_details.hostname,
        "PORT": database_details.port,
    }
}


@atexit.register
def goodbye():
    postgresql.stop()
