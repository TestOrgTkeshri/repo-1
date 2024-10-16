import os

import boto3

# EDIT THIS DEPENDING ON PROJECT
PROJECT = "repo-1"

DB_USERNAME_PROPERTY = "database.connection.username"
DB_HOST_PROPERTY = "database.connection.host"
DB_NAME_PROPERTY = "database.connection.name"

region = os.environ["REGION"] if "REGION" in os.environ else "us-west-2"

ssm = boto3.client("ssm", region)
rds = boto3.client("rds", region)

DB_PORT = "5432"
DB_USERNAME = ssm.get_parameter(Name="/{}/{}".format(PROJECT, DB_USERNAME_PROPERTY), WithDecryption=True)["Parameter"][
    "Value"]
DB_HOST = ssm.get_parameter(Name="/{}/{}".format(PROJECT, DB_HOST_PROPERTY), WithDecryption=True)["Parameter"]["Value"]
DB_NAME = ssm.get_parameter(Name="/{}/{}".format(PROJECT, DB_NAME_PROPERTY), WithDecryption=True)["Parameter"]["Value"]

# using iam for getting temporary password
DB_PASSWORD = rds.generate_db_auth_token(DBHostname=DB_HOST, Port=DB_PORT, DBUsername=DB_USERNAME, Region=region)
INSTALLED_APPS = [
    "django_models"
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = ["*"]
