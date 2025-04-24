from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        return render(request, 'admin/login.html', {'error': 'Неверные данные'})
    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required
def admin_tariffs(request):
    tariffs = Tariff.objects.select_related('region').all()
    return render(request, 'admin/tariff_list.html', {'tariffs': tariffs})

@login_required
def admin_toggle_tariff(request, tariff_id):
    tariff = get_object_or_404(Tariff, id=tariff_id)
    tariff.is_active = not tariff.is_active
    tariff.save()
    return redirect('admin_tariffs')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_requests(request):
    requests = ConnectionRequest.objects.select_related('tariff').order_by('-submitted_at')
    return render(request, 'admin/request_list.html', {'requests': requests})

@login_required
def admin_request_detail(request, request_id):
    conn_request = get_object_or_404(ConnectionRequest, id=request_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest._meta.get_field('status').choices):
            conn_request.status = new_status
            conn_request.save()
            return redirect('admin_requests')
    return render(request, 'admin/request_detail.html', {'request_obj': conn_request})

@login_required
def admin_update_request_status(request, request_id):
    if request.method == 'POST':
        conn_request = get_object_or_404(ConnectionRequest, id=request_id)
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest._meta.get_field('status').choices):
            conn_request.status = new_status
            conn_request.save()
    return redirect('admin_requests')

def admin_tariff_list(request):
    tariffs = Tariff.objects.all()
    return render(request, 'admin/tariff_list.html', {'tariffs': tariffs})

def admin_tariff_create(request):
    if request.method == 'POST':
        form = TariffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_tariffs')
    else:
        form = TariffForm()
    return render(request, 'admin/tariff_form.html', {'form': form, 'title': 'Добавить тариф'})

def admin_tariff_update(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    if request.method == 'POST':
        form = TariffForm(request.POST, instance=tariff)
        if form.is_valid():
            form.save()
            return redirect('admin_tariffs')
    else:
        form = TariffForm(instance=tariff)
    return render(request, 'admin/tariff_form.html', {'form': form, 'title': 'Редактировать тариф'})

def admin_tariff_delete(request, pk):
    tariff = get_object_or_404(Tariff, pk=pk)
    if request.method == 'POST':
        tariff.delete()
        return redirect('admin_tariffs')
    return render(request, 'admin/tariff_confirm_delete.html', {'tariff': tariff})


#Регионы
def manage_locations(request):
    regions = Region.objects.prefetch_related('localities').all()

    region_form = RegionForm()
    town_form = TownForm()

    if request.method == 'POST':
        if 'add_region' in request.POST:
            region_form = RegionForm(request.POST)
            if region_form.is_valid():
                region_form.save()
                return redirect('manage_locations')

        elif 'add_town' in request.POST:
            town_form = TownForm(request.POST)
            if town_form.is_valid():
                town_form.save()
                return redirect('manage_locations')

        elif 'delete_region' in request.POST:
            region_id = request.POST.get('region_id')
            region = get_object_or_404(Region, id=region_id)
            region.delete()
            return redirect('manage_locations')

        elif 'delete_town' in request.POST:
            town_id = request.POST.get('town_id')
            town = get_object_or_404(Town, id=town_id)
            town.delete()
            return redirect('manage_locations')

    return render(request, 'admin/manage_locations.html', {
        'regions': regions,
        'region_form': region_form,
        'town_form': town_form,
    })
