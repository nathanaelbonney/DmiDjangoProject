from django.contrib import admin
from createQuiz.models import *

class ChoiceInline(admin.StackedInline):
    model = Choice
    
class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [ChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Number of Times Taken',               {'fields': ['takers']}),
    ]
    inlines = [QuestionInline]
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('points',               {'fields': ['points']}),
    ]
    inlines = [ChoiceInline]
    
class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['answer']}),
        ('Is Correct',               {'fields': ['is_correct']}),
    ]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)