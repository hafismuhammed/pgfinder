from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    status = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    contact_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=100, choices=status, null=True)
    about = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pic', default="profile.png", null=True, blank=True)
    verify_otp = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Property(models.Model):
    category = (
        ('family', 'family'),
        ('boys', 'boys'),
        ('girls', 'girls'),
        ('any', 'any'),
    )

    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    types = models.CharField(max_length=100, choices=category, null=True)
    facilites = models.TextField()
    rent = models.CharField(max_length=200)
    deposite = models.CharField(max_length=100, null=True)
    images = models.FileField(upload_to='media/uploads',null=True)
    email = models.EmailField()
    mobile = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    notify = models.ManyToManyField(User, default=None, blank=True, related_name='notify')

    def __str__(self):
        return self.headline 


class Notifications(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    property = models.ForeignKey(Property, null=True, blank=True,on_delete=models.CASCADE)
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str_(self):
        return self.notification

