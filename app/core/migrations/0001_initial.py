# Generated by Django 3.2.6 on 2021-08-09 12:07

from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        CreateExtension('postgis')
    ]