from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import User_data
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
		)

class EditProfileFormExtra(forms.ModelForm):
	class Meta:
		model = User_data
		fields = (
			'image',
			'about',
			'github',
			'web_site',
			# 'work_or_study',
			# 'position',
			# 'where'
		)

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user