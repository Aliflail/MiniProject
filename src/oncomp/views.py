from datetime import timedelta
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed
from django.shortcuts import render,redirect,reverse, HttpResponseRedirect, get_object_or_404,HttpResponse
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
    template_name='ctest.html'
    def get(self,request,ctest_id):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        t=get_object_or_404(tmodels.Apt_Test,pk=(ctest_id))
        form = forms.AnswerForm()
        #
        # if not (Testscore.objects.filter(user=request.user,test=test).exists()) :
        #     score = Testscore.objects.create(user=request.user, test=test)
        #     request.session['Testscore_question']=1
        #     if test.apt_qns_set.filter(id=request.session['Testscore_question']).exists():
        #         q = test.apt_qns_set.get(id=request.session['Testscore_question'])
        #     else:
        #         while (request.session['Testscore_question'] <= test.apt_qns_set.count() and not (test.apt_qns_set.filter(id=request.session['Testscore_question']).exists())):
        #             request.session['Testscore_question'] +=1
        #         q = test.apt_qns_set.get(id=request.session['Testscore_question'])
        #     score.question=request.session['Testscore_question']
        #     score.itime = test.time
        #     context = {
        #         "q": q,
        #         "atest": score,
        #         "test_id": test_id
        #     }
        #     return render(request, self.template_name, context)
        # elif request.session.has_key('Testscore_question') and  test.apt_qns_set.filter(pk=request.session['Testscore_question']).exists():
        #     score = Testscore.objects.get(user=request.user, test=test)
        #     q = test.apt_qns_set.get(id=request.session['Testscore_question'])
        #     context = {
        #         "q": q,
        #         "atest":score,
        #         "test_id":test_id
        #     }
        #     return render(request,self.template_name,context)
        #
        #
        #
        #

        if not models.compilertestscore.objects.filter(user=request.user, test=t).exists() and t.compilerquestion_set.filter(pk=1).exists():
            request.session['compilerTestscore_question'] = 1
            if t.compilerquestion_set.filter(id=request.session['compilerTestscore_question']).exists():
                q = t.compilerquestion_set.get(pk=request.session['compilerTestscore_question'])
            else:
                while (request.session['compilerTestscore_question'] <= t.compilerquestion_set.count() and not (t.compilerquestion_set.filter(id=request.session['Testscore_question']).exists())):
                    request.session['compilerTestscore_question'] += 1
                q = t.compilerquestion_set.get(id=request.session['compilerTestscore_question'])
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
            while (request.session['compilerTestscore_question'] <= t.compilerquestion_set.count() and not (
                    t.compilerquestion_set.filter(id=request.session['compilerTestscore_question']).exists())):
                request.session['compilerTestscore_question'] += 1
            return HttpResponseRedirect(reverse("oncomp:ctest",args=(ctest_id)))
        else:
            while (request.session['compilerTestscore_question'] <= t.compilerquestion_set.count() and not (
                    t.compilerquestion_set.filter(id=request.session['compilerTestscore_question']).exists())):
                request.session['compilerTestscore_question'] += 1
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