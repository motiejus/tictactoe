# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('code', models.TextField(max_length=60000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e1', models.ForeignKey(to='contest.Entry', to_field='id')),
                ('e2', models.ForeignKey(to='contest.Entry', to_field='id')),
                ('round1', models.CharField(max_length=16, choices=[('e1', 'Entry 1 won'), ('e2', 'Entry 2 won'), ('draw', 'Draw'), ('Error', (('error1', 'Error by Entry 1'), ('error2', 'Error by Entry 2')))])),
                ('round2', models.CharField(max_length=16, choices=[('e1', 'Entry 1 won'), ('e2', 'Entry 2 won'), ('draw', 'Draw'), ('Error', (('error1', 'Error by Entry 1'), ('error2', 'Error by Entry 2')))])),
            ],
            options={
                'unique_together': set([('e1', 'e2')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('entry', models.ForeignKey(to='contest.Entry', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
