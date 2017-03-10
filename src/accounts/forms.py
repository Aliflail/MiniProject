from django import forms
from django.contrib.auth import authenticate, login ,logout,get_user_model
from .models import Profile
from tests import models
User=get_user_model()
class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    def clean(self):
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        user=authenticate(email=email,password=password)
        if not user:
            raise forms.ValidationError("THis user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
    
        return super(LoginForm,self).clean()

class ProfileForm(forms.ModelForm):
    admissionno=forms.CharField(max_length=7,widget=forms.TextInput(attrs={"class":"form-control"}))
    name=forms.CharField(max_length=14,widget=forms.TextInput(attrs={"class":"form-control"}))
    image=forms.FileField(widget=forms.FileInput(attrs={"type":"file" ,"accept":"image/*"," onchange":"loadFile(event)"}))
    class Meta:
        model= Profile
        fields=['admissionno','name','image','status']