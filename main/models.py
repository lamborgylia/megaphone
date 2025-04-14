from django.db import models

class Tariff(models.Model):
    title = models.CharField(max_length=255)  # Название тарифа
    price = models.IntegerField()
    old_price = models.IntegerField(blank=True, null=True)
    duration_days = models.IntegerField(default=30)
    internet_speed = models.CharField(max_length=100)
    mobile_gb = models.CharField(max_length=100, blank=True)
    tv_channels = models.CharField(max_length=100, blank=True)
    minutes = models.CharField(max_length=100, blank=True)
    options = models.TextField(blank=True)  # Например: "3 МегаСилы", "Домашний интернет"
    is_promo = models.BooleanField(default=False)
    promo_label = models.CharField(max_length=100, blank=True)
    button_color = models.CharField(max_length=20, default="#00B259")
    highlight_color = models.CharField(max_length=20, default="#F0F0F0")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
