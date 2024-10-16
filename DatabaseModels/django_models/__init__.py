import os
from typing import Any

import django
from django.db import connections

if os.environ.get('DJANGO_SETTINGS_MODULE', None) is None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
    django.setup()


def get_db_connection() -> Any:
    connection = connections["default"]
    connection.ensure_connection()
    return connection.connection
