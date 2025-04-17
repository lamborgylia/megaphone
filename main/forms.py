from django import forms
from .models import Tariff, Region, Town

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
            'megasila_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_home_internet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'megasila_count': 'Количество мегасилы',
            'region': 'Регион',
            'order': 'Порядок',
            'is_home_internet': 'Интернет для дома',
            'is_active': 'Активен',
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TownForm(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['name', 'region']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название региона'}),
        }

class TownForm(forms.ModelForm):
    class Meta:
        model = Town
        fields = ['name', 'region']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название города'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
        }
