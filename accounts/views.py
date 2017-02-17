from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views import View
# Create your views here.
class Indexpage(View):
    template_name='index.html'
    def get(self, request, *args):
        return render(request,self.template_name,{})