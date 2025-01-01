from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput(), label='password')

class XMLForm(forms.Form):
    archivo = forms.FileField(label='archivo')

class TextForm(forms.Form):
    textid = forms.CharField(label='textid')