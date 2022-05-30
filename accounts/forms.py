from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Customer


# Create your forms here.

class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)
	# name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	# def save(self, commit=True):
	# 	user = super(SignUpForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user
