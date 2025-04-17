from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('api/regions-towns/', views.get_regions_towns, name='regions_towns'),
    path('superadmin/login/', views_admin.admin_login, name='admin_login'),
    path('superadmin/logout/', views_admin.admin_logout, name='admin_logout'),
    path('superadmin/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('superadmin/tariffs/toggle/<int:tariff_id>/', views_admin.admin_toggle_tariff, name='admin_toggle_tariff'),
    path('superadmin/requests/', views_admin.admin_requests, name='admin_requests'),
    path('superadmin/requests/<int:request_id>/', views_admin.admin_request_detail, name='admin_request_detail'),
    path('superadmin/tariffs/', views_admin.admin_tariff_list, name='admin_tariffs'),
    path('superadmin/tariffs/create/', views_admin.admin_tariff_create, name='admin_tariff_create'),
    path('superadmin/tariffs/<int:pk>/edit/', views_admin.admin_tariff_update, name='admin_tariff_update'),
    path('superadmin/tariffs/<int:pk>/delete/', views_admin.admin_tariff_delete, name='admin_tariff_delete'),
    path('superadmin/locations/', views_admin.manage_locations, name='manage_locations'),
    path('api/regions-towns/', views.get_regions_towns, name='regions_towns'),
    path('api/tariffs/<int:region_id>/', views.get_tariffs_by_region, name='tariffs_by_region'),
    path('api/regions/', views.get_regions, name='regions'),
    path('api/towns/', views.get_towns, name='towns'),
    

] 
