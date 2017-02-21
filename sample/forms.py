from django import forms
from sample import models
class TestForm(forms.ModelForm):
    class Meta:
        model=models.Tests
        fields=['test_text','time','times']