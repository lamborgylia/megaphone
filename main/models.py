from django.db import models
import os

# models.py
class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(
        max_length=20,
        choices=[
            ('megafon', 'МегаФон'),
            ('rostelecom', 'Ростелеком')
        ],
        default='megafon'
    )

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='localities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'region']


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
    tv_channels = models.PositiveIntegerField(null=True, blank=True, help_text="Количество ТВ-каналов")
    megasila_count = models.PositiveIntegerField(null=True, blank=True)
    additional_number_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_megatariff = models.BooleanField(default=False, verbose_name="МегаТариф")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tariffs', verbose_name="Регион")
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='tariffs', null=True, blank=True, verbose_name="Город")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']  # сортировка по умолчанию
        
    def __str__(self):
        return f"{self.name} - {self.region.name}"

class ConnectionRequest(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # имя клиента
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
    request_type = models.CharField(
        max_length=20,
        choices=[
            ('connection', 'Подключение'),
            ('address_check', 'Проверка адреса')
        ],
        default='connection'
    )
    tariff = models.ForeignKey('Tariff', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} - {self.address[:30] if self.address else 'Без адреса'}"

# Предопределенное оборудование для каждого провайдера
MEGAFON_EQUIPMENT = [
    {
        'id': 'megafon-tv',
        'name': 'ТВ-приставка МегаФон',
        'description': 'Управляйте эфиром, перематывайте, ставьте на паузу — смотрите фильмы и сериалы как удобно.',
        'price': 3990,
        'image': 'img/equipment/megafon-tv.png',
        'is_installment': True,
        'coverage_area': 'до 100 м²',
        'features': [
            'Работает везде, где есть интернет',
            'Подключается через Wi-Fi',
            'Поддерживает видео UHD и HD',
            'Управляется Bluetooth-пультом'
        ]
    },
    {
        'id': 'megafon-router',
        'name': 'Роутер МегаФон',
        'description': 'Высокоскоростной роутер для стабильного интернета во всей квартире.',
        'price': 2990,
        'image': 'img/equipment/megafon-router.png',
        'is_installment': True,
        'coverage_area': 'до 150 м²',
        'features': [
            'Скорость до 1 Гбит/с',
            'Двухдиапазонный Wi-Fi',
            'Поддержка до 40 устройств',
            'Простая настройка'
        ]
    }
]

ROSTELECOM_EQUIPMENT = [
    {
        'id': 'rostelecom-tv',
        'name': 'ТВ-приставка Ростелеком',
        'description': 'Современная ТВ-приставка с поддержкой 4K и голосовым управлением.',
        'price': 3490,
        'image': 'img/equipment/rostelecom-tv.png',
        'is_installment': True,
        'coverage_area': 'до 120 м²',
        'features': [
            'Поддержка 4K Ultra HD',
            'Голосовое управление',
            'Встроенный Wi-Fi модуль',
            'Родительский контроль'
        ]
    },
    {
        'id': 'rostelecom-router',
        'name': 'Роутер Ростелеком',
        'description': 'Мощный роутер с поддержкой Wi-Fi 6 для максимальной производительности.',
        'price': 4990,
        'image': 'img/equipment/rostelecom-router.png',
        'is_installment': True,
        'coverage_area': 'до 200 м²',
        'features': [
            'Wi-Fi 6 (802.11ax)',
            'Гигабитные порты',
            'Поддержка Mesh-сети',
            'Приоритизация трафика'
        ]
    }
]

# Функция для получения оборудования по провайдеру
def get_equipment_by_provider(provider):
    if provider == 'megafon':
        return MEGAFON_EQUIPMENT
    elif provider == 'rostelecom':
        return ROSTELECOM_EQUIPMENT
    return []
