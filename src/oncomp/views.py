from django.shortcuts import render,reverse,redirect,HttpResponseRedirect,Http404,get_object_or_404
from django.views import View
from .models import Compilerquestion
from . import forms
from django.contrib.auth import get_user_model

from tests import models as tmodels
user =get_user_model()
class createtestview(View):
    def get(self,request):
        form=forms.QuestionForm()
        context={
            "form":form,
        }
        return render(request,'compiler.html',context)
class ctest(View):
    template_name='ctest.html'
    def get(self,request,ctest_id):
        t=get_object_or_404(tmodels.Apt_Test,pk=(ctest_id))
        q=t.compilerquestion_set.all()

        q=q.get(id=1)
        form=forms.AnswerForm()
        context={
            "q":q,
            "form":form
        }
        return render(request,self.template_name,context)
    def post(self,request,ctest_id):
        t = get_object_or_404(tmodels.Apt_Test, pk=(ctest_id))
        q = t.compilerquestion_set.all()
        q = q.get(id=1)
        form=forms.AnswerForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.uid=request.user
            f.tid=t
            f.qid=q
            f.save()
            return HttpResponseRedirect(reverse("accounts:home"))

        context = {
            "q": q,
            "form": form
        }
        return render(request, self.template_name, context)