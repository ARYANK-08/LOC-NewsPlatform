# forms.py
from django import forms
from .models import Question, Answer, Comment, Reply

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
