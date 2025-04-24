from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from .models import get_equipment_by_provider
from django.db.models import Case, When


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
    town_id = request.GET.get('town_id')
    
    # Base query for active tariffs in the region
    tariffs = Tariff.objects.filter(region=region, is_active=True)
    
    if town_id:
        # Filter by specific town or show tariffs available for all towns (town=None)
        tariffs = tariffs.filter(Q(town_id=town_id) | Q(town__isnull=True))
    
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
            'additional_number_price': float(tariff.additional_number_price) if tariff.additional_number_price else None,
            'tv_channels': tariff.tv_channels,
            'town_id': tariff.town_id if tariff.town else None
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

@require_http_methods(["GET"])
def get_towns_by_region(request, region_id):
    towns = Town.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(towns), safe=False)

def index(request):
    # Получаем текущий регион (можно из сессии или параметров)
    current_region = Region.objects.first()  # По умолчанию берем первый регион
    
    # Получаем оборудование для текущего региона
    equipment_list = get_equipment_by_provider(current_region.provider)
    
    context = {
        'current_region': current_region,
        'equipment_list': equipment_list,
    }
    return render(request, 'index.html', context)


def get_tariffs(request):
    region_id = request.GET.get('region_id')
    
    # Filter tariffs by region and active status
    tariffs = Tariff.objects.filter(
        is_active=True,
        region_id=region_id
    ).order_by('order')
    
    # Convert tariffs to JSON format
    tariffs_data = [{
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
        'additional_number_price': float(tariff.additional_number_price) if tariff.additional_number_price else None,
        'tv_channels': None  # Добавьте поле в модель если нужно
    } for tariff in tariffs]
    
    return JsonResponse({'tariffs': tariffs_data})

@require_http_methods(["POST"])
def create_connection_request(request):
    """API endpoint to create a new connection request."""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        phone_number = data.get('phone_number')
        address = data.get('address')
        tariff_id = data.get('tariff')
        
        # Validate required fields
        if not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)
            
        # Create connection request
        connection_request = ConnectionRequest(
            name=name,
            phone_number=phone_number,
            address=address
        )
        
        # Add tariff if provided
        if tariff_id:
            try:
                tariff = Tariff.objects.get(id=tariff_id)
                connection_request.tariff = tariff
            except Tariff.DoesNotExist:
                pass
        
        connection_request.save()
        
        return JsonResponse({
            'success': True,
            'id': connection_request.id
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def check_address(request):
    """API endpoint to check an address for connection availability."""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        address = data.get('address')
        
        # Validate required fields
        if not phone_number or not address:
            return JsonResponse({'error': 'Both phone number and address are required'}, status=400)
            
        # Create connection request with address check type
        connection_request = ConnectionRequest(
            phone_number=phone_number,
            address=address,
            request_type='address_check'
        )
        connection_request.save()
        
        return JsonResponse({
            'success': True,
            'id': connection_request.id
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_equipment_for_region(request, region_id):
    try:
        region = Region.objects.get(id=region_id)
        equipment = get_equipment_by_provider(region.provider)
        return JsonResponse({'equipment': equipment})
    except Region.DoesNotExist:
        return JsonResponse({'error': 'Region not found'}, status=404)

def search_cities(request):
    try:
        search_query = request.GET.get('query', '').strip().lower()  # Приводим запрос к нижнему регистру
        
        if len(search_query) < 2:
            return JsonResponse({
                'cities': [],
                'debug': {
                    'message': 'Query too short',
                    'query': search_query
                }
            })
        
        # Простой поиск без учета регистра
        cities = Town.objects.filter(
            name__icontains=search_query  # Поиск без учета регистра в любом месте названия
        ).select_related('region').distinct().order_by('name')[:10]
        
        results = []
        for city in cities:
            results.append({
                'id': city.id,
                'name': city.name,  # Оригинальное название города
                'region_id': city.region.id,
                'region_name': city.region.name
            })
        
        return JsonResponse({
            'cities': results,
            'debug': {
                'query': search_query,
                'total_found': len(results)
            }
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'cities': [],
            'error': str(e),
            'debug': {
                'query': search_query if 'search_query' in locals() else None,
                'traceback': traceback.format_exc()
            }
        }, status=500)