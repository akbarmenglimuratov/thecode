from django import forms
from questions.models import Question
from questions.models import Answer
from django.utils.translation import gettext_lazy as _
from pagedown.widgets import AdminPagedownWidget
from django.core.exceptions import ValidationError

class QuestionForm(forms.ModelForm):
	title = forms.CharField(label = 'Title')
	question_text = forms.CharField(widget=AdminPagedownWidget(attrs = {"cols": 100}))
	# tags = forms.CharField(, widget = forms.TextInput(attrs = {"placeholder": "A comma-separated list of tags. e.g python java php"}))
	class Meta:
		model = Question
		fields = ['title', 'question_text', 'tags']
		help_texts = {
            'tags': _('Add up to 5 tags to describe what your question is about'),
        }

	def clean(self):
		super().clean()
		tn = self.cleaned_data.get("tags")
		if len(tn) > 5:
			raise ValidationError("Invalid number of tags", code = "invalid")

class AnswerForm(forms.ModelForm):
	answer_text = forms.CharField(widget=AdminPagedownWidget(attrs = {'cols': 100}))
	class Meta:
		model = Answer
		fields = ['answer_text']