from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.views import View
from .models import Apt_Test,Testscore,Answers,Apt_Qns,Correct
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import TestForm,QuestionForm,AnswerForm,checkedAnswerform
from django.http import HttpResponseNotAllowed
from django.contrib import messages
import json
import datetime
from time import mktime

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)
# Create your views here.
user=get_user_model()

# class testpage(View):
#     template_name = "test.html"
#
#     def get(self, request, test_id):
#         test = get_object_or_404(Apt_Test, pk=test_id)
#
#         if Testscore.objects.filter(user=request.user).exists():
#             score = Testscore.objects.get(user=request.user, test=test)
#             request.session['Testscore_question']=score.question
#         else:
#             score = Testscore.objects.create(user=request.user, test=test)
#             request.session['Testscore_question']=score.question
#         if test.apt_qns_set.filter(pk=score.question).exists():
#             q=test.apt_qns_set.get(pk=request.session[['Testscore_question']])
#             context = {
#                 "q": q,
#                 "atest":test
#             }
#         else:
#             return HttpResponseRedirect(reverse('result',args=(test_id)))
#         return render(request, self.template_name, context)
#
#     def post(self, request, test_id):
#         test = get_object_or_404(Apt_Test, pk=test_id)
#         if Testscore.objects.filter(user=request.user).exists():
#             score = Testscore.objects.get(user=request.user, test=test)
#         else:
#             score = Testscore.objects.create(user=request.user, test=test)
#
#         try:
#             q=test.apt_qns_set.get(pk=score.question)
#             selected_choice = q.answers_set.get(pk=request.POST['choice'])
#         except(KeyError, Answers.DoesNotExist):
#             context = {
#                 "t": test,
#                 "error": "you didnt select a choice"
#             }
#             return render(request, self.template_name, context)
#         else:
#             print(request.POST['choice'])
#             if selected_choice.correct_set.all().exists():
#                 score.score += 1
#                 score.question+=1
#                 score.save()
#                 return HttpResponseRedirect(reverse('test', args=(test_id)))
#
#             else:
#
#                 score.question+=1
#                 score.save()
#                 return HttpResponseRedirect(reverse('test', args=(test_id)))


class testpage(View):
    template_name = "test.html"

    def get(self, request, test_id):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        test = get_object_or_404(Apt_Test, pk=test_id)

        if not Testscore.objects.filter(user=request.user,test=test).exists():
            score = Testscore.objects.create(user=request.user, test=test)

            request.session['time'] = json.dumps(test.time, cls=MyEncoder)
            request.session['Testscore_question']=score.question

            print request.session['time']

        if request.session.has_key('Testscore_question') and  test.apt_qns_set.filter(pk=request.session['Testscore_question']).exists():
            q=test.apt_qns_set.get(pk=request.session['Testscore_question'])

            context = {
                "q": q,
                "atest":request.session['time']
            }
        else:
            return HttpResponseRedirect(reverse('result',args=(test_id)))
        return render(request, self.template_name, context)

    def post(self, request, test_id):
        test = get_object_or_404(Apt_Test, pk=test_id)
        if Testscore.objects.filter(user=request.user).exists():
            score = Testscore.objects.get(user=request.user, test=test)
        else:
            score = Testscore.objects.create(user=request.user, test=test)

        try:
            q=test.apt_qns_set.get(pk=request.session['Testscore_question'])
            selected_choice = q.answers_set.get(pk=request.POST['choice'])
        except(KeyError, Answers.DoesNotExist):
            context = {
                "t": test,
                "error": "you didnt select a choice"
            }
            return render(request, self.template_name, context)
        else:
            print(request.POST['choice'])
            if selected_choice.correct_set.all().exists():
                score.score += 1
                request.session['Testscore_question']+=1
                score.save()
                return HttpResponseRedirect(reverse('test', args=(test_id)))

            else:

                request.session['Testscore_question']+= 1
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
        return render(request, self.createtestt, {"tform": TestForm()})

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

