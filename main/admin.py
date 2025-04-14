# admin.py
from django.contrib import admin
from .models import Tariff

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "old_price", "is_promo")
    list_editable = ("price", "old_price", "is_promo")
