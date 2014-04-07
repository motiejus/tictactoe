# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0002_fight'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('entry', models.ForeignKey(to_field='id', to='contest.Entry')),
            ],
            options={
                'verbose_name_plural': 'Latest Entries',
            },
            bases=(models.Model,),
        ),
    ]
