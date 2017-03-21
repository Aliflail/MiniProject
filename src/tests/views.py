from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.views import View
from .models import Apt_Test,Testscore,Answers,Apt_Qns,Correct
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import TestForm,QuestionForm,AnswerForm,checkedAnswerform
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from datetime import timedelta
from accounts import models
from oncomp import models as omodels
from django.http import JsonResponse
user=get_user_model()
class testpage(View):
    template_name = "test.html"
    def get(self, request, test_id):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        test = get_object_or_404(Apt_Test, pk=test_id)
        if not (Testscore.objects.filter(user=request.user,test=test).exists()) :
            score = Testscore.objects.create(user=request.user, test=test)
            request.session['Testscore_question']=1
            if test.apt_qns_set.filter(id=request.session['Testscore_question']).exists():
                q = test.apt_qns_set.get(id=request.session['Testscore_question'])
            else:
                while (request.session['Testscore_question'] <= test.apt_qns_set.count() and not (test.apt_qns_set.filter(id=request.session['Testscore_question']).exists())):
                    request.session['Testscore_question'] +=1
                q = test.apt_qns_set.get(id=request.session['Testscore_question'])
            score.question=request.session['Testscore_question']
            score.itime = test.time
            context = {
                "q": q,
                "atest": score,
                "test_id": test_id
            }
            return render(request, self.template_name, context)
        elif request.session.has_key('Testscore_question') and  test.apt_qns_set.filter(pk=request.session['Testscore_question']).exists():
            score = Testscore.objects.get(user=request.user, test=test)
            q = test.apt_qns_set.get(id=request.session['Testscore_question'])
            context = {
                "q": q,
                "atest":score,
                "test_id":test_id
            }
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect(reverse('oncomp:ctest',args=(test_id)))
    def post(self, request, test_id):
        test = get_object_or_404(Apt_Test, pk=test_id)
        if Testscore.objects.filter(user=request.user).exists():
            score = Testscore.objects.get(user=request.user, test=test)
        else:
            score = Testscore.objects.create(user=request.user, test=test)
        try:
            q=test.apt_qns_set.get(pk=request.session['Testscore_question'])
            print request.POST['time']
            score.itime=timedelta(seconds=int(request.POST['time']))
            selectedchoice = q.answers_set.get(pk=request.POST['choice'])
        except(KeyError, Answers.DoesNotExist):
            context = {
                "t": test,
                "error": "you didnt select a choice"
            }
            return render(request, self.template_name, context)
        else:
            if selectedchoice.correct_set.all().exists():
                score.score += 1
                request.session['Testscore_question'] += 1
                if test.apt_qns_set.filter(id=request.session['Testscore_question']).exists():
                    q = test.apt_qns_set.get(id=request.session['Testscore_question'])
                else:
                    while (request.session['Testscore_question'] <= test.apt_qns_set.count() and not (test.apt_qns_set.filter(id=request.session['Testscore_question']).exists())):
                        request.session['Testscore_question'] += 1
                    score.save()
                return HttpResponseRedirect(reverse('test', args=(test_id)))
            else:
                request.session['Testscore_question'] += 1
                if test.apt_qns_set.filter(id=request.session['Testscore_question']).exists():
                    q = test.apt_qns_set.get(id=request.session['Testscore_question'])
                else:
                    while (request.session['Testscore_question'] <= test.apt_qns_set.count() and not (test.apt_qns_set.filter(id=request.session['Testscore_question']).exists())):
                        request.session['Testscore_question'] += 1
                    score.save()
                return HttpResponseRedirect(reverse('test', args=(test_id)))
class resultpage(View):
    template_name="results.html"
    def get(self,request,test_id):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        test = get_object_or_404(Apt_Test, pk=test_id)
        score = get_object_or_404(Testscore, test=test,user=request.user)
        context={
            "score":score,
        }
        return render(request,self.template_name,context)
class createtest(View):
    createtestt = "createtest.html"
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        return render(request, self.createtestt, {"tform": TestForm(),
                                                  "profile":models.Profile.objects.get(user=request.user),
                                                  "createlink":"active"})
    def post(self, request):
        t = TestForm(request.POST)
        if t.is_valid():
            object = t.save()
            request.session['Apt_Test_id'] = object.id
            messages.success(request, ' test created ')
            return redirect(reverse('createquestion'))
class createquestion(View):
    createquestion = "createquestions.html"
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        q = QuestionForm({"test_id":request.session['Apt_Test_id']})
        return render(request,self.createquestion,{"qform":q})
    def post(self,request):
        q=QuestionForm(request.POST)
        if q.is_valid():
            t=q.save()
            request.session['Apt_Qns_id']= t.id
            messages.success(request, 'answer created ')
            return redirect(reverse('createanswer'))
        return render(request, self.createquestion, {"qform": q})
class createanswer(View):
    createanswer = "createanswers.html"
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        a=checkedAnswerform({"qn_id":request.session['Apt_Qns_id']})
        return render(request,self.createanswer,{"aform":a})
    def post(self,request):
        a = checkedAnswerform(request.POST)
        if a.is_valid():
            if request.POST.get('islast'):
                t = a.save()
                if request.POST.get('iscorrect'):
                    q=Apt_Qns.objects.get(id=request.session['Apt_Qns_id'])
                    Correct.objects.create(ans_id=t, qn_id=q)
                return redirect(reverse('accounts:home'))
            else:
                if request.POST.get('nextq'):
                    t = a.save()
                    if request.POST.get('iscorrect'):
                        q = Apt_Qns.objects.get(id=request.session['Apt_Qns_id'])
                        Correct.objects.create(ans_id=t, qn_id=q)
                    return redirect(reverse('createquestion'))
                else:
                    t = a.save()
                    if request.POST.get('iscorrect'):
                        q = Apt_Qns.objects.get(id=request.session['Apt_Qns_id'])
                        Correct.objects.create(ans_id=t, qn_id=q)
                    return redirect(reverse('createanswer'))
        else:
            return redirect(reverse('createanswer'))
def testexpire(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    request.session['Testscore_question'] = 0
    return HttpResponse('Sorry expired')
def updatetime(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    test = get_object_or_404(Apt_Test, pk=request.POST["test_id"])
    score = Testscore.objects.get(user=request.user, test=test)
    score.itime = timedelta(seconds=int(request.POST["timer"]))
    score.save()
    return HttpResponse("ok")