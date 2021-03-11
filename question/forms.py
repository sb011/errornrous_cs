from django.forms import ModelForm
from question.models import *
from django import forms
from question.models import Question, Answer


class AddQuestionForm(ModelForm):
    class Meta:
        model = Question
        field = ('title', 'question', 'auth')
        exclude = ['Question']


class AddAnswerForm(ModelForm):
    class Meta:
        model = Answer
        field = ('answer', 'question', 'auth')
        exclude = ['Answer']


class QuestionUpdateForm(ModelForm):
    class Meta:
        model = Question
        field = ('title', 'question', 'auth')
        exclude = ['Question']


class AnswerUpdateForm(ModelForm):
    class Meta:
        model = Answer
        field = ('answer', 'question', 'auth')
        exclude = ['Answer']
