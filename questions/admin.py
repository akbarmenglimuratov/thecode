from django.contrib import admin
from . import models
from django.contrib.auth.models import User

class AnswerData(admin.ModelAdmin):
	list_display = ['id', 'user', 'date', 'verified']


class QuestionData(admin.ModelAdmin):
    list_display = ['title', 'question_text', 'fav_count', 'date']

class CommentData(admin.ModelAdmin):
	list_display = ['id', 'user', 'comment_text', 'date']

admin.site.register(models.Comment, CommentData)
admin.site.register(models.Question, QuestionData)
admin.site.register(models.Answer, AnswerData)