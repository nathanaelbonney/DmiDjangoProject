from django import forms
from django.forms import ModelForm
from createQuiz.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.util import help_text_for_field

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        
class DisplayQuestionForm(forms.Form):
    choices = forms.ModelChoiceField(queryset=Quiz.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(DisplayQuestionForm, self).__init__(*args, **kwargs)
        self.choices = queryset=self.instance.choice_set.all()

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, help_text="Optional.", required=False)
    last_name = forms.CharField(max_length=30, help_text="Optional.", required=False)
    password1 = forms.CharField(label="Password", min_length=6, help_text="At least 6 characters.", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", min_length=6, help_text="Repeat your password.", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
        