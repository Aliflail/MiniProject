from datetime import timedelta
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed
from django.shortcuts import render,reverse, HttpResponseRedirect, get_object_or_404,HttpResponse
from django.views import View
from oncomp.compiler import main
from tests import models as tmodels
from . import forms
from . import models
user =get_user_model()
class createtestview(View):
    def get(self,request):
        form=forms.QuestionForm()
        context={
            "form":form,
        }
        return render(request,'compiler.html',context)
class ctest(View):
    template_name='ctest.html'#alif noushad
    def get(self,request,ctest_id):
        t=get_object_or_404(tmodels.Apt_Test,pk=(ctest_id))
        form = forms.AnswerForm()
        if not models.compilertestscore.objects.filter(user=request.user, test=t).exists() and t.compilerquestion_set.filter(pk=1).exists():
            request.session['compilerTestscore_question'] = 1
            q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
            score = models.compilertestscore.objects.create(user=request.user, test=t,question=q)
            # we can eventually add the times in the respective question but for now this will do
            score.itime = q.time
            # ..
            context = {
                "q": q,
                "ctest": score,
                "ctest_id": ctest_id,
                "form": form
            }
            return render(request, self.template_name, context)
        elif request.session.has_key('compilerTestscore_question') and t.compilerquestion_set.filter(
                pk=request.session['compilerTestscore_question']).exists():
            q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
            score = models.compilertestscore.objects.get(user=request.user, test=t, question=q)
            context = {
                "q": q,
                "ctest": score,
                "ctest_id": ctest_id,
                "form": form
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse('result', args=(ctest_id)))
    def post(self,request,ctest_id):
        t = get_object_or_404(tmodels.Apt_Test, pk=(ctest_id))
        if not models.compilertestscore.objects.filter(user=request.user, test=t).exists():
            return HttpResponseRedirect(reverse("oncomp:ctest", args=(ctest_id)))
        else:
            score = models.compilertestscore.objects.get(user=request.user, test=t)
        form=forms.AnswerForm(request.POST)
        q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
        if form.is_valid():
            f=form.save(commit=False)
            f.uid=request.user
            f.tid=t
            f.qid=q
            f.save()
            request.session['compilerTestscore_question']+=1
            objects= main.process(f.program, q.pname, f.language, q.mark, q.id, request.user)
            mark=objects.core()
            #compilation and mark
            #score will be used for mark calculations
            return HttpResponseRedirect(reverse("oncomp:ctest",args=(ctest_id)))
        else:
            return HttpResponseRedirect(reverse("oncomp:ctest", args=(ctest_id)))
def ctestexpire(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    request.session['compilerTestscore_question'] = 0
    return HttpResponse('Sorry expired')
def cupdatetime(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    test = get_object_or_404(tmodels.Apt_Test, pk=request.POST["ctest_id"])
    score =models.compilertestscore.objects.get(user=request.user, test=test)
    score.itime = timedelta(seconds=int(request.POST["timer"]))
    score.save()
    return HttpResponse("ok")