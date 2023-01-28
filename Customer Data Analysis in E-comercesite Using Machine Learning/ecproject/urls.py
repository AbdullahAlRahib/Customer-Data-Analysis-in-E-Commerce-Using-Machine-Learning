from django.contrib import admin
from django.urls import path, include
# from django.conf.urls path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('customadmin/', include('customer_prediction.urls')),
]
