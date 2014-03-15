# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='fights',
            field=models.ManyToManyField(blank=True, to='contest.Fight'),
            preserve_default=True,
        ),
    ]
