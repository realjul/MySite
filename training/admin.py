from django.contrib import admin
from .models import Exam, Question, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'job','passing_score','date_created')
    inlines = [QuestionInLine]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'order')
    inlines = [ChoiceInline]

