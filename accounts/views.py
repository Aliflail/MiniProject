from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views import View
from accounts.admin import UserCreationForm
from django.contrib.auth import authenticate, login ,logout
from accounts.models import MyUser
from accounts.forms import LoginForm
# Create your views here.
class Indexpage(View):
    template_name='index.html'
    def get(self, request, *args):
        form=LoginForm()
        return render(request,self.template_name,{"form":form})
    def post(self,request, *args):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/')
        return render(request, self.template_name, {"form": form})
class Registerpage(View):
    template_name='register.html'
    def get(self, request, *args):
        form=UserCreationForm()
        context={
            "form":form,
        }
        return render(request,self.template_name,context)

    def post(self, request, *args):
        form = UserCreationForm(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request,user)
                return redirect('/home/')

        return render(request, self.template_name, context)
class Homepage(View):
    template_name='home.html'
    def get(self,request,*args):
        return render(request,self.template_name,{})