# Additional
from django.utils import timezone
from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.http import Http404, JsonResponse

# Tags items
from taggit.models import Tag

# Models
from .models import Question
from django.contrib.auth.models import User
from accounts.models import User_data
from .models import Answer
from notifications.signals import notify

# Forms
from django import forms
from questions.forms import QuestionForm 
from questions.forms import AnswerForm 


# views, templates
from django.views import View
from django.views.generic import DetailView, TemplateView, FormView, CreateView
# from hitcount.views import HitCountMixin, HitCountDetailView


# Tags data
class TagListView(TemplateView):
	template_name = 'questions/tag_list.html'
	model = Tag

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['tags'] = Tag.objects.all()
		except Tag.DoesNotExist:
			context['tags'] = []
		return context



class TaggedQuestionView(TemplateView):
	template_name = 'questions/tags.html'
	model = Question

	def get_absolute_url(self):
		return reverse('article_detail', kwargs={'slug': self.slug})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['data'] = Question.objects.filter(tags__name__in = [kwargs['slug']]).all()
		except Tag.DoesNotExist:
			context['data'] = {}
		return context

class tagListView(TemplateView):
	model = Tag
	template_name = 'questions/tag_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['tags'] = Tag.objects.all()
		except Tag.DoesNotExist:
			context['tags'] = {}
		return context

# All question list
class QuestionView(TemplateView):
	model = Question
	template_name = 'questions/questions.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['data'] = Question.objects.all().order_by('-date')[:20]
		except Question.DoesNotExist:
			context['data'] = {}
		return context

# Ask question
class AskQuestion(CreateView):
	template_name = "questions/ask_question.html"
	model = Question
	form_class = QuestionForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = QuestionForm()
		return context

	def form_valid(self, form):
		if self.request.user.is_authenticated == True:
			if form.is_valid():
				obj = form.clean()
				obj = form.save(commit = False)
				obj.date = timezone.now()
				obj.user = self.request.user
				obj.save()
				form.save_m2m()
				addToUserQuestionField = User_data.objects.get(username = self.request.user)
				addToUserQuestionField.question.add(obj)
				return super().form_valid(form)
		else:
			return redirect('/accounts/login/') 

# For question data
# Show question datas==================================================================================
class QuestionDetailView(CreateView):
	template_name = 'questions/question_data.html'
	model = Question
	form_class = AnswerForm

	def get_success_url(self, **kwargs):
		project = self.get_object()
		return project.get_absolute_url()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['data'] = self.get_object()
		context['form'] = AnswerForm()
		return context

	def form_valid(self, form):
		if self.request.user.is_authenticated == True:
			obj = form.clean()
			obj = form.save(commit = False)
			obj.date = timezone.now()
			obj.user = self.request.user
			obj.save()
			question_to_save = self.get_object().answer.add(obj)
			return super().form_valid(form)
		else:
			return redirect('/accounts/login/')



# Vote To Question=======================================================================================
class VoteToQuestionClass(View):
	def get(self, request, pk, vote):
		self.request = request
		self.data = {}
		self.pk = int(pk)
		self.vote = int(vote)
		if self.vote == 1 or self.vote == 0:
			return JsonResponse(self.get_question_data())
		else:
			return self.error()

	def get_question_data(self):
		try:
			self.obj = Question.objects.get(pk = self.pk)
			if self.obj.user != self.request.user:
				return self.voter_exist()
			else:
				self.data['success'] = False
				self.data['message'] = "You can't vote your own question!"
				return self.data
		except Question.DoesNotExist:
			raise Http404("Question does not exist!")

	def voter_exist(self):
		if not self.obj.voters.filter(pk = self.request.user.id).exists():
			return self.add_user_to_voters()
		else:
			self.data["success"] = False
			self.data["message"] = "You already voted!"
			return self.data

	def add_user_to_voters(self):
		self.obj.voters.add(self.request.user.id)
		if self.vote == 1:
			self.obj.vote_up = self.obj.vote_up + 1
		elif self.vote == 0:
			self.obj.vote_down = self.obj.vote_down + 1

		self.obj.vote_point = self.obj.vote_up - self.obj.vote_down
		self.obj.save()
		return self.reputation()

	def reputation(self):
		rep = User_data.objects.get(username = self.obj.user)
		self.data["success"] = True
		if self.vote == 1:
			rep.reputation = rep.reputation + 5
			self.data["message"] = "You voted up!"
			self.data["notify_message"] = "Your question voted up!"
		elif self.vote == 0:
			rep.reputation = rep.reputation - 2
			self.data["message"] = "You voted down!"
			self.data["notify_message"] = "Your question voted down!"
		rep.save()
		print(self.data['notify_message'])
		notify.send(self.request.user, recipient=self.obj.user, verb=self.data["notify_message"], level = "info")
		return self.data

	def error(self):
		self.data['success'] = False
		self.data['message'] = "Something went wrong!"
		return self.data

#Vote to Answer=========================================================================================
class VoteToAnswerClass(View):
	def get(self, request, pk, vote_value):
		self.request = request
		self.data = {}
		l = int(vote_value)
		self.vote, self.val = l%10, l//10
		if self.vote == 1 or self.vote == 0:
			return JsonResponse(self.get_answer_data())
		else:
			return self.error()
	def get_answer_data(self):
		try:
			self.obj = Answer.objects.get(pk = self.val)
			if self.obj.user != self.request.user:
				return self.voter_exist()
			else:
				self.data['success'] = False
				self.data['message'] = "You can't vote your own answer!"
				return self.data
			return self.voter_exist()
		except Answer.DoesNotExist:
			raise Http404("Answer does not exist!")
	def voter_exist(self):
		if not self.obj.voters.filter(pk = self.request.user.id).exists():
			return self.add_user_to_voters()
		else:
			self.data['success'] = False
			self.data['message'] = "You already voted!"
			return self.data
	def add_user_to_voters(self):
		self.obj.voters.add(self.request.user.id)
		if self.vote == 1:
			self.obj.vote_up = self.obj.vote_up + 1
		elif self.vote == 0:
			self.obj.vote_down = self.obj.vote_down + 1

		self.obj.vote_point = self.obj.vote_up - self.obj.vote_down
		self.obj.save()
		return self.reputation()
	def reputation(self):
		rep = User_data.objects.get(username = self.obj.user)
		self.data["success"] = True
		if self.vote == 1:
			rep.reputation = rep.reputation + 10
			self.data["message"] = "You voted up!"
			self.data["notify_message"] = "Your answer voted up!"
		elif self.vote == 0:
			rep.reputation = rep.reputation - 2
			self.data["message"] = "You voted down!"
			self.data["notify_message"] = "Your answer voted down!"
		rep.save()
		notify.send(self.request.user, recipient=self.obj.user, verb=self.data["notify_message"], level = "info")
		return self.data
	def error(self):
		self.data['success'] = False
		self.data['message'] = "Something went wrong!"
		return self.data

# Add question to favorite=================================================================================
class AddQuestionToFavorite(View):
	
	def get(self, request, pk):
		self.request = request
		if self.request.is_ajax():
			self.pk = int(pk)
			self.data = {}
			return JsonResponse(self.get_user_data())
		else:
			raise Http404("Page does not exist")

	def get_user_data(self):
		try:
			self.obj = User_data.objects.get(pk = self.request.user.id)
			if not self.obj.question.filter(pk = self.pk).exists():
				return self.add_favorite()
			else:
				self.data['success'] = False
				self.data['message'] = "You can't add your own question to favorite!"
				return self.data
		except User_data.DoesNotExist:
			raise Http404("Page does not exist!")

	def add_favorite(self):
		if not self.obj.fav_question.filter(pk = self.pk).exists():
			self.data["success"] = True
			self.data["message"] = "Added to favorite!"
			self.obj.fav_question.add(self.pk)
		else:
			self.data["success"] = False
			self.data["message"] = "Deleted from favorite!"
			self.obj.fav_question.remove(self.pk)
		self.obj.save()
		return self.data