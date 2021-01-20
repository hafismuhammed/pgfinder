from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField



class Profile(models.Model):
    status = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    contact_number = PhoneNumberField()
    address = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=100, choices=status, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

class Property(models.Model):

    catogery = (
        ('family', 'Family'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('any', 'Any')
    )

    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    types = models.CharField(max_length=100, choices=catogery, null=True)
    facilites = models.TextField(null=True)
    rent = models.FloatField()
    deposit = models.FloatField()
    images = models.FileField(upload_to='media/uploads', null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, null=True)
    is_booked = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.headline 

class PropertyImages(models.Model):
    owner = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, null=True, blank=False, on_delete=models.CASCADE, related_name='propertyimg')
    image = models.FileField(upload_to='media/uploads', null=False)

    def __str__(self):
        return self.property.headline
    

class Notifications(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    property = models.ForeignKey(Property, null=True, blank=True,on_delete=models.CASCADE)
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str_(self):
        return self.notification



class PayingGuestCheckout(models.Model):
    paying_guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255, null=True, default=None)
    total_amount = models.FloatField()
    payment_signature = models.CharField(max_length=255, null=True, default=None)
    reciept_num = models.CharField(max_length=255)
    payment_completed =  models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)


class BookedProperty(models.Model):
    paying_guest = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    checkout_details = models.ForeignKey(PayingGuestCheckout, on_delete=models.CASCADE, null=False, blank=False)
    property_location = models.CharField(max_length=255)
    property_rent = models.FloatField()
    property_address = models.CharField(max_length=200)

    