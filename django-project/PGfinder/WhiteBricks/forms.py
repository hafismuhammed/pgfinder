from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from WhiteBricks.models import User, Property, Profile

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

class PasswordChangeForm(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput())
    newpassword = forms.CharField(widget=forms.PasswordInput())
    conformpassword = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User

gender = (
    ("M", "Male"),
    ("F", "Femle"),
)

class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    contact_number = forms.IntegerField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=gender, required=False)
    occupation = forms.CharField(widget=forms.TextInput(), required=False)
    address = forms.CharField(widget=forms.TextInput(), required=False)
    about = forms.CharField(widget=forms.Textarea(attrs={'cols':10, 
    'rows': 5}), required=False)
    profile_pic = forms.FileField(widget=forms.FileInput(), required=False)
    
types = (
    ("family", "Family"),
    ('boys', "Boys"),
    ("girls", "Girls"),
    ("any", "Any")
)

class AccomodationForm(forms.Form):
    headline = forms.CharField(widget=forms.TextInput(), required=True)
    city = forms.CharField(widget=forms.TextInput(), required=True)
    location = forms.CharField(widget=forms.TextInput(), required=True)
    address = forms.CharField(widget=forms.TextInput())
    types = forms.ChoiceField(choices=types, required=False)
    facilites = forms.CharField(widget=forms.Textarea(attrs={'cols':10, 
    'rows': 5,'palceholder':'facilites'}), required=True)
    rent = forms.CharField(widget=forms.TextInput(), required=True)
    deposite = forms.CharField(widget=forms.TextInput(), required=True)
    images = forms.FileField(widget=forms.FileInput(), required=True)
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    mobile = forms.IntegerField(widget=forms.TextInput(), required=True)

    class Meta:
        model = property

   