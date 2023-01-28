from django.db import models


STATUS_CHOICES = (
    ('high', 'high'),
    ('medium', 'medium'),
    ('low', 'low')
)


class DeliveryDetails(models.Model):
    customer_care_call =models.IntegerField()
    customer_rating =models.IntegerField()
    product_cost=models.IntegerField()
    no_of_pur =models.IntegerField()
    product_importance = models.CharField(max_length=50, choices=STATUS_CHOICES, default='high')
    offer_discount =models.IntegerField()
    weight =models.IntegerField()

    def __str__(self):
        return str(self.id)


class AnnualSpending(models.Model):
    avg_sess =models.FloatField()
    avg_spend_time_app =models.FloatField()
    avg_spend_time_web =models.FloatField()
    mem_len =models.FloatField()

    def __str__(self):
        return str(self.id)