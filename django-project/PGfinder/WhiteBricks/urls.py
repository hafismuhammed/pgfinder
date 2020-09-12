from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .tokens import account_activation_token
 
urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('my_property/', views.my_property, name='my_property'),
    path('register/', views.Register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logingout, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('insert/', views.add_property, name='new_property'),
    path('search/', views.search, name='search'),
    path('property_type', views.property_list, name='property_type'),
    path('forgot', views.forgot_password, name='forgot_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('property_details/<int:requested_id>', views.property_previw, name='property_details'),
    path('edit_property/<int:requested_property_id>', views.edit_property, name='edit_property'),
    path('delete_property/<int:requested_id>', views.delete_property, name='delete_property'),
    path('contact_details/', views.contact_details, name='contact_details'),
    path('notification', views.notification, name='notification'),
    path('veiw_notification', views.view_notification, name='view_notification'),
    path('delete_notification', views.delete_notification, name='delete_notification'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('admin_contact', views.admin_contact, name='admin_msg'),
    path('coustemer_info/<int:requested_id>', views.coustemer_info, name='coustemer_info'),
    path('coustemer_info/delete_property/<int:requested_id>', views.delete_coust_pro, name='del_coust_pro'),
    ]

   
