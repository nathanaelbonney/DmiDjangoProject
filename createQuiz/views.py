from django.shortcuts import get_object_or_404, render
from django.http import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views import generic
from createQuiz.models import *
from datetime import datetime
from createQuiz.forms import *
from django.contrib.auth import authenticate, login, logout

def QuizQuestions(request):
#     return HttpResponse("hello")
    return render(request, 'createQuiz/UXproject.html', {'user': request.user})

def SubmitQuiz(request):
    if 'numQuestions' in request.POST:
        quiz = Quiz.objects.create(name=request.POST['quizName'], pub_date=datetime.now())
        if request.user.is_authenticated():
            quiz.author = request.user
        quiz.save()
        for i in range (1, int(request.POST['numQuestions']) + 1):
            question = quiz.question_set.create(text=request.POST['questionText' + str(i)], points=int(request.POST['points' + str(i)]))
            for j in range (1, int(request.POST['select' + str(i)]) + 1):
                choice = question.choice_set.create(answer=request.POST['q' + str(i) + 'a' + str(j)])
                if j == int(request.POST['correct' + str(i)]):
                    choice.is_correct = True;
                choice.save()
            question.save()
        return render(request, 'createQuiz/SubmitQuiz.html', {'quizURL':request.build_absolute_uri(reverse('createQuiz.views.TakeQuiz', args=(quiz.id,)))})
    
    else:
        return HttpResponse("No questions found. Please resubmit your quiz.")
     
def TakeQuiz(request, quizId):
    quiz = Quiz.objects.filter(id=quizId)
    if quiz.count() > 0:
        quiz = quiz[0]
        if request.user == quiz.author:
            return HttpResponse("You created this quiz! Why do you want to take it?")
        elif request.user in quiz.takers.all() and not request.user.is_anonymous():
            return HttpResponse("Sorry, you already took this quiz.")
        else:
            quizForm = QuizForm(instance=quiz)
            return render(request, 'createQuiz/FinishedTest.html', {'quiz': quiz, 'quizForm': quizForm})
    else: 
        return HttpResponse("Sorry, we could not find your quiz.")
        
def GradeQuiz(request, quizId):
    quiz = Quiz.objects.filter(id=quizId)
    if quiz.count() > 0:
        quiz = quiz[0]
        if request.user in quiz.takers.all() and not request.user.is_anonymous():
            return HttpResponse("Sorry, you already took this quiz.")
        elif request.user not in quiz.takers.all() and not request.user.is_anonymous():
            quiz.takers.add(User.objects.filter(id=request.user.id)[0])
        else:
            pass
#           quiz.save(update_fields=['takers'])
        numQuestions = quiz.question_set.all().count()
        pointsTotal = 0
        pointsEarned = 0
        questionAnswers = []
        for i in range(1, numQuestions + 1):
            question = quiz.question_set.all()[i - 1]
            pointsTotal += question.points
            questionAnswers.append([question, request.POST['q' + str(i)]])
            if question.choice_set.filter(is_correct=True)[0].answer == request.POST['q' + str(i)]:
                pointsEarned += question.points
        percentage = float(pointsEarned) / pointsTotal
        return render(request, 'createQuiz/displayResults.html', {'quiz': quiz, 'pointsEarned' : pointsEarned, 'pointsTotal' : pointsTotal, 'percentageCorrect' : "{0:.2f}%".format(percentage * 100), 'questionAnswers' : questionAnswers})
#         return HttpResponse(log + "You got " + str(pointsEarned) + " out of " + str(pointsTotal) + " points.")
    else: 
        return HttpResponse("Sorry, we could not find your quiz to grade.")

def LoginScreen(request, url):
    return render(request, 'createQuiz/login.html', {"incorrectLogin" : "", "url" : url})

def Login(request, url):
    username = request.POST['user']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/create/") #replace with proper URL later
        else:
            return HttpResponse("Sorry, your account has been disabled.")
    else:
        return render(request, 'createQuiz/login.html', {"incorrectLogin" : "Sorry, your username and password combination was incorrect", "url" : url[:-1]})
    
def Register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/create/")
    else:
        form = CreateUserForm()
    return render(request, "createQuiz/register.html", {
        'form': form,
    })
    
def Logout(request):
    logout(request)
    return HttpResponseRedirect("/create/") #replace with home URL later

@login_required(login_url='/create/login/')
def Profile(request):
    quizes = Quiz.objects.filter(author=request.user)
    return render(request, 'createQuiz/userProfile.html', {'user': request.user, 'quizlist': quizes})