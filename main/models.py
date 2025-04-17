from django.db import models

# models.py
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='localities')

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Tariff(models.Model):
    name = models.CharField(max_length=255)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    is_home_internet = models.BooleanField(default=False)
    home_internet_note = models.CharField(max_length=255, null=True, blank=True)
    speed_mbps = models.PositiveIntegerField(null=True, blank=True)
    minutes = models.PositiveIntegerField(null=True, blank=True)
    gigabytes = models.PositiveIntegerField(null=True, blank=True)
    megasila_count = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tariffs')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']  # сортировка по умолчанию
        
    def __str__(self):
        return f"{self.name} - {self.region.name}"

class ConnectionRequest(models.Model):
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)  # не обязательное поле
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'Новая'),
            ('in_progress', 'В работе'),
            ('done', 'Обработана')
        ],
        default='new'
    )
    tariff = models.ForeignKey('Tariff', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} - {self.address[:30] if self.address else 'Без адреса'}"
