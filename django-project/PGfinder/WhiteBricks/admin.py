from django.contrib import admin
from .models import Property, Notifications, Profile, BookingDetails



admin.site.site_header = "WhiteBricks Admin Dashboard"
admin.site.title = "WhiteBricks"

class CustProperty(admin.ModelAdmin):
    list_display = ('owner', 'headline', 'city', 'location', 'address', 'is_booked')
    list_display_links = ('headline',)
    list_editable = ('is_booked',)
    search_fields = ('location', 'city')
    ordering = ['id']
    list_filter = ('types', 'date', )

class CustBookingDetails(admin.ModelAdmin):
    list_display = ('user', 'property', 'first_name', 'last_name', 'email', 'mobile', 'date')
    ordering = ['date']
    list_filter = ('property', 'date', )
    search_fields = ('user', 'property')
    
# Register your models here for admin control.

admin.site.register(Profile)
admin.site.register(Property, CustProperty)
admin.site.register(BookingDetails, CustBookingDetails)



