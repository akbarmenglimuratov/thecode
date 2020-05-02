from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import User_data
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, View
# from hitcount.views import HitCountDetailView
from accounts.forms import EditProfileForm, EditProfileFormExtra

class Profile(TemplateView):
	model = User_data
	template_name = "account/profile.html"
	def dispatch(self, request, *args, **kwargs):
	    if not self.request.user.is_authenticated:
	        return redirect('/accounts/login/')

	    return super(Profile, self).dispatch(request, *args, **kwargs)


class GetUserData(DetailView):
	model = User_data
	template_name = 'account/user.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['data'] = self.get_object()
		return context

class GetUsersList(TemplateView):
	model = User_data
	template_name = 'account/user_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['data'] = User_data.objects.all().order_by('-reputation')
		return context

class Edit(View):
	template_name = 'account/edit.html'
	form_class = EditProfileFormExtra
	initial = {'key': 'value'}

	def get(self,request):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form })

	def post(self, request, **kwargs):
		form = self.form_class(request.POST, request.FILES,  instance = request.user.user_data)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/edit/')
		else:
			print(False)
		return render(request, self.template_name, {'form': form})
