# Generated by Django 3.1.4 on 2020-12-27 12:39

from django.db import migrations
import os
import sys

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(open(os.path.join(sys.path[0], 'raw.sql'), 'r').read())
    ]
