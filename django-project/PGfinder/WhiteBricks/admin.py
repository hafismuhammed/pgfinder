from django.contrib import admin
from .models import Property, Notifications, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Property)
admin.site.register(Notifications)


