from django.forms import ModelForm
from django import forms
from main.models import User

class SignupForm(ModelForm):

    def create_user(self):
        user = User.objects.create_user(username=self.cleaned_data.get("username"), email=self.cleaned_data.get("email"), password=self.cleaned_data.get("password"))
	return user

    class Meta:
        model = User
	fields = ["username", "password", "email"]
