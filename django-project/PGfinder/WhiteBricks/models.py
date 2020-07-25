from django.db import models
from django.contrib.auth.models import User



class Property(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    facilites = models.TextField()
    rent = models.CharField(max_length=200)
    images = models.FileField(upload_to='media/uploads',null=True)
    email = models.EmailField()
    mobile = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    notify = models.ManyToManyField(User, default=None, blank=True, related_name='Liked')

    def __str__(self):
        return self.headline 


class Notifications(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    property = models.ForeignKey(Property, null=True, blank=True,on_delete=models.CASCADE)
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str_(self):
        return self.notification

