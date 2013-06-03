from django.conf.urls import patterns, include, url

from createQuiz import views
from django.http.response import HttpResponse

urlpatterns = patterns('',
    url(r'/submitquiz/', views.SubmitQuiz, name="SubmitQuiz"),
    url(r'', views.QuizQuestions, name='makeQuiz'),
)