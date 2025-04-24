from django import forms
from .models import *

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'home_internet_note': forms.TextInput(attrs={'class': 'form-control'}),
            'speed_mbps': forms.NumberInput(attrs={'class': 'form-control'}),
            'minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'gigabytes': forms.NumberInput(attrs={'class': 'form-control'}),
            'tv_channels': forms.NumberInput(attrs={'class': 'form-control'}),
            'megasila_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_number_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'town': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_home_internet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_megatariff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название тарифа',
            'old_price': 'Старая цена',
            'current_price': 'Текущая цена',
            'duration_days': 'Продолжительность (дни)',
            'home_internet_note': 'Примечание к интернету',
            'speed_mbps': 'Скорость (Мбит/с)',
            'minutes': 'Минуты',
            'gigabytes': 'Гигабайты',
            'tv_channels': 'ТВ-каналы',
            'megasila_count': 'Количество мегасилы',
            'additional_number_price': 'Цена за дополнительный номер',
            'region': 'Регион',
            'town': 'Город',
            'order': 'Порядок',
            'is_home_internet': 'Интернет для дома',
            'is_active': 'Активен',
            'is_megatariff': 'МегаТариф',
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название региона'
            })
        }
        labels = {
            'name': 'Название региона'
        }

class TownForm(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['name', 'region']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название города'
            }),
            'region': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'name': 'Название города',
            'region': 'Регион'
        }

# class EquipmentForm(forms.ModelForm):
#     class Meta:
#         model = Equipment
#         fields = ['name', 'description', 'price', 'rental_period', 'is_installment', 
#                  'coverage_area', 'image', 'is_active']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#             'price': forms.NumberInput(attrs={'step': '0.01'}),
#         }
