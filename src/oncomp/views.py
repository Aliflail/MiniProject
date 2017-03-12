from django.shortcuts import render,reverse,redirect,HttpResponseRedirect,Http404,get_object_or_404,HttpResponse
from django.views import View
from . import models
from . import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed
from datetime import timedelta
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
        form = forms.AnswerForm()

        if not models.compilertestscore.objects.filter(user=request.user, test=t).exists():
            score = models.compilertestscore.objects.create(user=request.user, test=t)
            request.session['compilerTestscore_question'] = score.question
            # we can eventually add the times in the respective question but for now this will do
            q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
            score.itime = q.time
            # ..
        else:


            score = models.compilertestscore.objects.get(user=request.user, test=t)

        if request.session.has_key('compilerTestscore_question') and t.compilerquestion_set.filter(
                pk=request.session['compilerTestscore_question']).exists():
            q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
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
