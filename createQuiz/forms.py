from django import forms
from django.forms import ModelForm
from createQuiz.models import *

class quiz(forms.Form):
    name = forms.CharField()

class createQuestion(forms.Form):
    text = forms.CharField()

class displayQuestion(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)