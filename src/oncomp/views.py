from django.shortcuts import render,reverse,redirect,HttpResponseRedirect,Http404
from django.views import View
from . import models
from . import forms
from tests import models as tmodels
class createtestview(View):
    def get(self,request):
        form=forms.QuestionForm()
        context={
            "form":form,
        }
        return render(request,'compiler.html',context)