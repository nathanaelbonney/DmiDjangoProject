from django.shortcuts import get_object_or_404, render
from django.http import *
from django.core.urlresolvers import reverse
from django.views import generic
from createQuiz.models import *
from datetime import datetime

def QuizQuestions(request):
#     return HttpResponse("hello")
    return render(request, 'createQuiz/UXproject.html')

def SubmitQuiz(request):
    if 'numQuestions' in request.POST:
        quiz = Quiz(name=request.POST['quizName'], pub_date=datetime.now(), author="Nathanael", num_takers=0)
        quiz.save()
        for i in range (1, int(request.POST['numQuestions']) + 1):
            question = quiz.question_set.create(text=request.POST['questionText' + str(i)], points=int(request.POST['points' + str(i)]))
            for j in range (1, int(request.POST['select' + str(i)]) + 1):
                choice = question.choice_set.create(answer=request.POST['q' + str(i) + 'a' + str(j)])
                if j == int(request.POST['correct' + str(i)]):
                    choice.is_correct = True;
                choice.save()
            question.save()
#         return HttpResponse("Quiz Submitted")
        return render(request, 'createQuiz/FinishedTest.html', {'quiz': quiz})
    
    else:
        return HttpResponse("No questions found. Please resubmit your quiz.")