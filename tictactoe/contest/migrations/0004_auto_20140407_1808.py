# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_latestentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 4, 7, 18, 8, 23, 959301), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fight',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 4, 7, 18, 8, 28, 908912), auto_now_add=True),
            preserve_default=False,
        ),
    ]
