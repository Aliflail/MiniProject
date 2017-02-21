from django.shortcuts import render
from django.views import View
from sample import models ,forms
class samplepage(View):
	"""docstring for samplepage"""
	def  get(self,request):
		t=models.Tests.objects.all()
		f=forms.TestForm()
		q=models.Question.objects.all()
		context={
			"question":q,
			"test": t,
			"testform":f
		}
		return render(request,'sample.html',context)
	def post(self,request):
		t = models.Tests.objects.all().get(pk=2 )
		f = forms.TestForm()
		q=t.question_set.all()

		context = {
			"question": q,

			"test": t,
			"testform": f
		}
		f = forms.TestForm(request.POST)
		f.save()
		return render(request,'sample.html',context)