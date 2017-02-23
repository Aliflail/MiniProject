from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views import View
from accounts.admin import UserCreationForm
from django.contrib.auth import authenticate, login ,logout
from .forms import ProfileForm
from accounts.forms import LoginForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
user =get_user_model()
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
        profile=ProfileForm()
        context={
            "form":form,
            "profile":profile,
        }
        return render(request,self.template_name,context)

    def post(self, request, *args):
        form = UserCreationForm(request.POST)
        profile = ProfileForm(request.POST)
        context = {
            "form": form,
            "profile":profile,

        }


        if form.is_valid() and profile.is_valid():
            user = form.save()
            pro= profile.save(commit=False)
            pro.user=user
            pro.slug=slugify(pro.name)
            pro.save()
            if pro is not None:
                login(request,user)
                return redirect('/home/')

        return render(request, self.template_name, context)
class Homepage(View):
    template_name='home.html'
    def get(self,request,*args):
        p=Profile.objects.get(user=request.user)
        return render(request,self.template_name,{"profile":p})
def logoutview(request):
    logout(request)
    return redirect('/')
    from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='redirecting',login_url='')

def profileview(request,slug):
    p = Profile.objects.get(slug=slug)
    return render(request,'profile.html',{"profile":p})