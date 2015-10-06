from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField(label="email", max_length=30, required=True)
	password = forms.CharField(label="password", required=True, widget=forms.PasswordInput)