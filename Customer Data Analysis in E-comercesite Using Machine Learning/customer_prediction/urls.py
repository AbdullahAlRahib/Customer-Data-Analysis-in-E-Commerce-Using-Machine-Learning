# from django.conf.urls import url
from django.urls import path
from customer_prediction import views

from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    # path('', views.IndexView, name='index'),
    
    
    
    path('', admin_login, name='adminlogin'), #login
    path('customlogout/', logout_view, name='customlogout'), #logout
    path('dashboard/', admindashboard, name='admindashboard'), #dashboard
    path('order/', order, name='order'),
    



    
    path('single_churn/', views.SingleChurnView, name='single_churn'),
    path('total_churn/', views.TotalChurnView, name='total_churn'),
    path('single_spending/', views.SingleSpendingView, name='single_spending'),
    path('total_spending/', views.TotalSpendingView, name='total_spending'),
    path('single_delivery/', views.SingleDeliveryView, name='single_delivery'),
    path('total_delivery/', views.TotalDeliveryView, name='total_delivery'),
    #path('musician_details/<pk>/', views.IndexVie.as_view(), name='musician_details'),
    
]
