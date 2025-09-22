from django.contrib.auth.models import AbstractUser
from django.db import models
from provision.utils.snowflake import snowflake


def generate_snowflake_id():
    return snowflake.generate()


class User(AbstractUser):   
    id = models.BigIntegerField(
        primary_key=True,
        default=generate_snowflake_id,
        editable=False
    )