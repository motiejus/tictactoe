# encoding: utf8
from django.db import models, migrations
from django.conf import settings
import challenge.tools.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('code', models.TextField(validators=[challenge.tools.validators.ByteLengthValidator(60000)])),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('e1', models.ForeignKey(to='contest.Entry', to_field='id')),
                ('e2', models.ForeignKey(to='contest.Entry', to_field='id')),
                ('round1', models.CharField(choices=[('e1', 'Entry 1 won'), ('e2', 'Entry 2 won'), ('draw', 'Draw'), ('Error', (('error1', 'Error by Entry 1'), ('error2', 'Error by Entry 2')))], max_length=16)),
                ('round2', models.CharField(choices=[('e1', 'Entry 1 won'), ('e2', 'Entry 2 won'), ('draw', 'Draw'), ('Error', (('error1', 'Error by Entry 1'), ('error2', 'Error by Entry 2')))], max_length=16)),
            ],
            options={
                'unique_together': set([('e1', 'e2')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('entry', models.ForeignKey(to='contest.Entry', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
