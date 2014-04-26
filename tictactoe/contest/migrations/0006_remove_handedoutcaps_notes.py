# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_handedoutcaps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='handedoutcaps',
            name='notes',
        ),
    ]
