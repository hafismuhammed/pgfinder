from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('master_config', views.master_config, name='master_config'),
    path('master_config_update2', views.master_config_update2, name='master_config_update2'),
    path('add_product', views.add_product, name='add_product'),
    path('signup', views.signup, name='signup'),
    path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('sales_bill/', views.sales_bill, name='sales_bill'),
    path('ajax_calls/product_bill/', views.product_bill, name='product_bill'),
    path('ajax_calls/product_bill_id/', views.product_bill_id, name='product_bill_id'),
    path('ajax_calls/search/', views.autocompleteModel, name='autocompleteModel'),
    path('sales_bill_submit/', views.sales_bill_submit, name='sales_bill_submit'),
]