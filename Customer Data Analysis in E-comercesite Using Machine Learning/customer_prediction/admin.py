from django.contrib import admin
from .models import (
    DeliveryDetails,
    AnnualSpending,
)

# Register your models here.


@admin.register(DeliveryDetails)
class DeliveryDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_care_call','customer_rating', 'product_cost', 'no_of_pur', 'product_importance', 'offer_discount', 'weight']


@admin.register(AnnualSpending)
class AnnualSpendingModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'avg_sess', 'avg_spend_time_app', 'avg_spend_time_web', 'mem_len']
