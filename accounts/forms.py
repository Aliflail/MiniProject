from django import forms
from django.contrib.auth import authenticate, login ,logout,get_user_model
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
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active")
        return super(LoginForm,self).clean()
