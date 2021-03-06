# Generated by Django 3.0.5 on 2020-04-22 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='num_vote_down',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='num_vote_up',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='vote_score',
        ),
        migrations.RemoveField(
            model_name='question',
            name='num_vote_down',
        ),
        migrations.RemoveField(
            model_name='question',
            name='num_vote_up',
        ),
        migrations.RemoveField(
            model_name='question',
            name='vote_score',
        ),
        migrations.AddField(
            model_name='answer',
            name='vote_down',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='vote_point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='vote_up',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
