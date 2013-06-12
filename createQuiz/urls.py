from django.conf.urls import patterns, include, url

from createQuiz import views
from django.http.response import HttpResponse

urlpatterns = patterns('',
    url(r'/login/(?P<url>\S*$)', views.LoginScreen, name="Login"),
    url(r'/submitlogin/(?P<url>\S*)$', views.Login, name="SubmitLogin"),
    url(r'/submitquiz/', views.SubmitQuiz, name="SubmitQuiz"),
    url(r'/register/', views.Register, name="Register"),
    url(r'/takeQuiz/(?P<quizId>\d+)$', views.TakeQuiz, name="TakeQuiz"),
    url(r'/gradeQuiz/(?P<quizId>\d+)$', views.GradeQuiz, name="GradeQuiz"),
    url(r'/logout/', views.Logout, name="Logout"),
    url(r'/profile/', views.Profile, name="Profile"),
    url(r'', views.QuizQuestions, name='makeQuiz'),
)