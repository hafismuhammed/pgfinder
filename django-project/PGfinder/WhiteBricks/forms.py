from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from WhiteBricks.models import  Property, Profile, BookingDetails


gender = (
    ("---", "---"),
    ("M", "Male"),
    ("F", "Female"),
)

class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    contact_number = PhoneNumberField(widget=forms.TextInput(), required=True)
    gender = forms.ChoiceField(choices=gender, required=False)
    occupation = forms.CharField(widget=forms.TextInput(), required=False)
    address = forms.CharField(widget=forms.TextInput(), required=False)
    
types = (
    ("---", "---"),
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
    rent = forms.FloatField(widget=forms.NumberInput(), required=True)
    deposite = forms.FloatField(widget=forms.NumberInput(), required=True)
    images = forms.FileField(widget=forms.FileInput(), required=True)
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    mobile = forms.CharField(widget=forms.TextInput(), required=True)

    class Meta:
        model = property

class BookingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(), required=True)
    last_name = forms.CharField(widget=forms.TextInput(), required=True) 
    email_address = forms.EmailField(widget=forms.EmailInput(), required=True) 
    mobile_number = PhoneNumberField(widget=forms.TextInput(), required=True)

    class Meta:
        model = BookingDetails