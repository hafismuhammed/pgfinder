from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .tokens import account_activation_token
 
urlpatterns = [
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('portfolio/', views.MyProperty, name='portfolio'),
    path('register/', views.Register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logingout, name='logout'),
    #path('insert/', views.Adverticement, name='myad'),
    path('search/', views.search, name='search'),
    
    #path(
    #    'reset_password/',
    #    auth_views.PasswordResetView.as_view(
    #        template_name='myhome/reset_password.html',
    #        html_email_template_name='myhome/reset_password_email.html',
    #        success_url=settings.LOGIN_URL,
     #       token_generator=account_activation_token),
     #       name='reset_password'
  #  ),
    #path(
    #    'reset_password_conformation/<str:uidb64>/<str:token>/',
    #    auth_views.PasswordResetConfirmView.as_view(
    #        template_name='myhome/reset_password_update.html',
    #        post_reset_login=True,
    #        post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
    #        token_generator=account_activation_token,
    #        success_url=settings.LOGIN_REDIRECT_URL),
    #        name='password_reset_confirm'
    #    ),
    path('edit_property/<int:requested_property_id>', views.edit_property, name='edit_property'),
    path('delete_property/<int:requested_id>', views.delete_property, name='delete_property'),
    path('contact_details/', views.contact_details, name='contact_details'),
    path('login_api', views.login_api, name='login_api'),
    # testing ajax
    path('test_ajax', views.sample_ajax_view, name='test-ajax'),
    path('ajax_template', views.sample_view, name='sample_view'),

        # test password reser
    
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='myhome/reset_password.html'),  name='reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.as_view(template_name='myhome/reset_email_sent.html'), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='myhome/reset_password_update.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='myhome/password_reset_done.html'), name='password_reset_complete'),
    ]