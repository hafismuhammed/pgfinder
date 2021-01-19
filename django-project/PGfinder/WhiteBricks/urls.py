from django.conf import settings
from django.urls import path
from . import views
from .tokens import account_activation_token
 
urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('my_property/', views.my_properties, name='my_property'),
    path('register/', views.user_register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('insert/', views.add_property, name='new_property'),
    path('search/', views.search_properties, name='search'),
    path('property_type', views.list_properties, name='property_type'),
    path('forgot', views.forgot_password, name='forgot_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('property_details/<int:requested_id>', views.property_detailview, name='property_details'),
    path('edit_property/<int:requested_property_id>', views.edit_property, name='edit_property'),
    path('delete_property/<int:requested_id>', views.delete_property, name='delete_property'),
    path('contact_details/<int:requested_id>', views.contact_details, name='contact_details'),
    path('notification/<int:requested_id>', views.notification, name='notification'),
    path('veiw_notification', views.view_notifications, name='view_notification'),
    path('delete_notification', views.delete_notifications, name='delete_notification'),
    path('booking_details/<int:requested_id>', views.booking_details, name='booking_details'),
    path('payment_success', views.make_payment, name='payment_success'),

    path('room-booking/<int:requested_id>', views.room_booking, name='room_booking'),
    path('payment-confirmation', views.mark_pymentsuccess, name='payment_confirmation'),
]

   
