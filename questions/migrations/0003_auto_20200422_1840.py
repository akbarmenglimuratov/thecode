# Generated by Django 3.0.5 on 2020-04-22 15:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0002_auto_20200422_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(default=None, related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
