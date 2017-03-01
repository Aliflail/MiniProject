from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.views import View
from .models import Apt_Test,Testscore,Answers,Apt_Qns
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your views here.
user=get_user_model()

# class testpage(View):
#     template_name="tests.html"
#     def get(self,request,test_id):
#         test=get_object_or_404(Apt_Test,pk=test_id)
#
#         context={
#             "test":test
#         }
#         return render(request,self.template_name,context)
#     def post(self,request,test_id):
#         test = get_object_or_404(Apt_Test, pk=test_id)
#         if Testscore.objects.filter(user=request.user).exists():
#             score = Testscore.objects.get(user=request.user, test=test)
#         else:
#             score = Testscore.objects.create(user=request.user, test=test)
#         try:
#             q = test.apt_qns_set.get(pk=request.POST['question'])
#             selected_choice = q.answers_set.get(pk=request.POST['choice'])
#         except(KeyError,Answers.DoesNotExist):
#             context = {
#                 "t": test,
#                 "error": "you didnt select a choice"
#             }
#             return render(request, self.template_name, context)
#         else:
#             if selected_choice.correct_set.filter(pk=request.POST['choice']).exists() :
#
#                 if q.correct_set.get(pk=request.POST['question']) == selected_choice.correct_set.get(pk=request.POST['choice']):
#                     score.score += 1
#                     score.save()
#                     return HttpResponseRedirect(reverse('test', args=(test_id)))
#
#             else:
#                 return HttpResponseRedirect(reverse('test', args=(test_id)))


class testpage(View):
    template_name = "test.html"

    def get(self, request, test_id):
        test = get_object_or_404(Apt_Test, pk=test_id)
        if Testscore.objects.filter(user=request.user).exists():
            score = Testscore.objects.get(user=request.user, test=test)
        else:
            score = Testscore.objects.create(user=request.user, test=test)

        if test.apt_qns_set.filter(pk=score.question).exists():
            q=test.apt_qns_set.get(pk=score.question)
            context = {
                "q": q
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
            q=test.apt_qns_set.get(pk=score.question)
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
                score.question+=1
                score.save()
                return HttpResponseRedirect(reverse('test', args=(test_id)))

            else:

                score.question+=1
                score.save()
                return HttpResponseRedirect(reverse('test', args=(test_id)))

class resultpage(View):
    template_name="results.html"
    def get(self,request,test_id):
        test = get_object_or_404(Apt_Test, pk=test_id)
        score = get_object_or_404(Testscore, test=test)
        context={
            "score":score,
        }
        return render(request,self.template_name,context)