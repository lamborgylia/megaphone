from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


@require_http_methods(["GET"])
def get_regions_towns(request):
    """API endpoint to get all regions with their towns."""
    regions_data = {}
    regions = Region.objects.all().prefetch_related('localities')
    
    for region in regions:
        towns = [town.name for town in region.localities.all()]
        regions_data[region.name] = towns
    
    return JsonResponse(regions_data)

@require_http_methods(["GET"])
def get_tariffs_by_region(request, region_id):
    """API endpoint to get tariffs for a specific region."""
    region = get_object_or_404(Region, id=region_id)
    tariffs = Tariff.objects.filter(region=region, is_active=True)
    
    tariffs_data = []
    for tariff in tariffs:
        tariff_data = {
            'id': tariff.id,
            'name': tariff.name,
            'old_price': float(tariff.old_price) if tariff.old_price else None,
            'current_price': float(tariff.current_price),
            'duration_days': tariff.duration_days,
            'is_home_internet': tariff.is_home_internet,
            'home_internet_note': tariff.home_internet_note,
            'speed_mbps': tariff.speed_mbps,
            'minutes': tariff.minutes,
            'gigabytes': tariff.gigabytes,
            'megasila_count': tariff.megasila_count,
            # Add TV channels field for filtering
            'tv_channels': 250 if 'ТВ' in tariff.name or tariff.name == 'МегаФон 3.0 МегаТариф' else None
        }
        tariffs_data.append(tariff_data)
    
    return JsonResponse(tariffs_data, safe=False)

@require_http_methods(["GET"])
def get_regions(request):
    """API endpoint to get regions, with optional name filter."""
    name_filter = request.GET.get('name', '')
    
    if name_filter:
        regions = Region.objects.filter(name__icontains=name_filter)
    else:
        regions = Region.objects.all()
    
    regions_data = [{'id': region.id, 'name': region.name} for region in regions]
    return JsonResponse(regions_data, safe=False)

@require_http_methods(["GET"])
def get_towns(request):
    """API endpoint to get towns, with optional name filter."""
    name_filter = request.GET.get('name', '')
    
    if name_filter:
        towns = Town.objects.filter(name__icontains=name_filter).select_related('region')
    else:
        towns = Town.objects.all().select_related('region')[:100]  # Limit to 100 towns if no filter
    
    towns_data = [
        {
            'id': town.id, 
            'name': town.name, 
            'region_id': town.region.id,
            'region_name': town.region.name
        } 
        for town in towns
    ]
    return JsonResponse(towns_data, safe=False)


def index(request):
    return render(request, 'index.html')


def get_regions_towns(request):
    # Get all regions with their towns
    regions_data = {}
    
    regions = Region.objects.all().order_by('name')
    for region in regions:
        towns = region.localities.all().order_by('name')
        regions_data[region.name] = [town.name for town in towns]
    
    return JsonResponse(regions_data)