from django import forms
from django.contrib.auth import authenticate, login ,logout,get_user_model
from . import models
class TestForm(forms.ModelForm):
    class Meta:
        model=models.Apt_Test
        fields=['time','name','endDate']
class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Apt_Qns
        fields=['question','test_id']


class AnswerForm(forms.ModelForm):
    class Meta:
        model=models.Answers
        fields=['answer','qn_id']

class checkedAnswerform(AnswerForm):
    iscorrect =forms.BooleanField(label="is this the correct answer?",initial=False ,required=False)
    islast = forms.BooleanField(label="is this last answer for last question?",initial=False ,required=False)
    nextq=forms.BooleanField(label="get next question",initial=False ,required=False)
    class Meta(AnswerForm.Meta):
        fields = AnswerForm.Meta.fields+['islast']+['iscorrect']+['nextq']
