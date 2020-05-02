# Generated by Django 3.0.5 on 2020-04-22 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0003_auto_20200422_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='vote_down',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='vote_point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='vote_up',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(default=None, related_name='question_voters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(default=None, related_name='answer_voters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
