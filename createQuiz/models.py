from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):

    name = models.CharField(max_length=128)
    author = models.ForeignKey(User, blank = True, null = True, related_name='authorUser')
    pub_date = models.DateTimeField()
    takers = models.ManyToManyField(User, blank = True, null = True, related_name='takerUser')

    def __unicode__(self):
        return self.name
    
class Question(models.Model):
    
    quiz = models.ForeignKey(Quiz)
    text = models.CharField(max_length=512)
    points = models.IntegerField(default=10)
    
    def __unicode__(self):
        return self.text
    
class Choice(models.Model):
    
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=128)
    is_correct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.answer