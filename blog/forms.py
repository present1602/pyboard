from .models import Question
from django import forms
from django.forms import Textarea


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text':Textarea(attrs={'cols':5, 'rows':3})
        }

