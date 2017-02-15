from django.shortcuts import render
from django.views import View
# Create your views here.
class Indexpage(View):
    template_name ="index.html"
    def get(self,request):
        return render(request,self.template_name,{})