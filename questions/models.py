from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
# from hitcount.models import HitCount, HitCountMixin
from django.urls import reverse
from taggit.managers import TaggableManager

class Answer(models.Model):
	answer_text = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "answer_user")
	date = models.DateTimeField()
	vote_point = models.IntegerField(default = 0)
	vote_up = models.IntegerField(default = 0)
	vote_down = models.IntegerField(default = 0)
	voters = models.ManyToManyField(User, related_name = "answer_voters")
	verified = models.BooleanField(default = False)

	def get_absolute_url(self):
		return reverse('questions:question_datas', kwargs={'pk': self.pk})

class Comment(models.Model):
	comment_text = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	date = models.DateTimeField()


class Question(models.Model):
	title = models.TextField()
	question_text = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "question_user")
	date = models.DateTimeField()
	answer = models.ManyToManyField(Answer)
	tags = TaggableManager()
	comment = models.ManyToManyField(Comment)
	vote_point = models.IntegerField(default = 0)
	vote_up = models.IntegerField(default = 0)
	vote_down = models.IntegerField(default = 0)
	voters = models.ManyToManyField(User, related_name = "question_voters", default = None)
	fav_count = models.IntegerField(default = 0)
	# hit_count_generic = GenericRelation(
 #        HitCount, object_id_field='object_pk',
 #        related_query_name='hit_count_generic_relation')

	def get_absolute_url(self):
		return reverse('questions:question_datas', kwargs={'pk': self.pk})


