# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('x', models.ForeignKey(to_field='id', to='contest.Entry')),
                ('o', models.ForeignKey(to_field='id', to='contest.Entry')),
                ('gameplay', models.CommaSeparatedIntegerField(max_length=230, help_text="Gameplay flow. Board is separated to 81 cells. Each number means a move by alternating player. For example, '10,1,0' means: x placed (2,1,1,1), o placed (1,1,1,1) and x made an error. In case 0 is at the end (like in the example), 'error' field is non-empty.")),
                ('error', models.CharField(max_length=255, help_text="Non-empty if `gameplay' ends with zero", blank=True)),
                ('result', models.CharField(max_length=10, help_text='Fight result of x (e1) versus o (e2). Relative to e1.', choices=[('win', 'win'), ('draw', 'draw'), ('loss', 'loss')])),
            ],
            options={
                'unique_together': set([('x', 'o')]),
                'index_together': set([('x', 'result'), ('o', 'result')]),
            },
            bases=(models.Model,),
        ),
    ]
