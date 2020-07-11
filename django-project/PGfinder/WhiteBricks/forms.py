from django import forms
from django.contrib.auth.forms import UserCreationForm
from WhiteBricks.models import User, Property

class RegistraionForm(UserCreationForm):
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User

class AccomodationForm(forms.Form):
    headline = forms.CharField(widget=forms.TextInput(), required=True)
    city = forms.CharField(widget=forms.TextInput(), required=True)
    location = forms.CharField(widget=forms.TextInput(), required=True)
    facilites = forms.CharField(widget=forms.Textarea(attrs={'cols':10, 
    'rows': 5,'palceholder':'facilites'}), required=True)
    rent = forms.CharField(widget=forms.TextInput(), required=True)
    images = forms.FileField(widget=forms.FileInput(), required=True)
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    mobile = forms.IntegerField(widget=forms.TextInput(), required=True)

    class Meta:
        model = property