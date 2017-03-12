from django import forms
from django.contrib.auth import authenticate, login ,logout,get_user_model
from . import models
class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Compilerquestion
        fields=['prog','pname','mark','test_id','time']
class AnswerForm(forms.ModelForm):
    program=forms.CharField(widget=forms.Textarea(attrs={"class":"hidden"}))
    class Meta:
        model=models.canswer
        fields=['program','language']