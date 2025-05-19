from django.urls import path, re_path
from . import views
from . import auth_views
from . import car_views
from .crud_views import (
    CrudIndex,
    CarTypeList, CarTypeCreate, CarTypeUpdate, CarTypeDelete,
    PartTypeList, PartTypeCreate, PartTypeUpdate, PartTypeDelete,
    PartList, PartCreate, PartUpdate, PartDelete,
    ServiceList, service_update, service_create, ServiceDelete,
    ServiceTypeCreate, ServiceTypeList, ServiceTypeUpdate, ServiceTypeDelete
)
from .statistics_view import statistics_view

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('faq/', views.glossary_view, name='glossary'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('confidential_policy/', views.policy, name='policy'),
    path('career/', views.vacancy_list, name='career'),
    path('register/client/', auth_views.register_client, name='register_client'),
    path('login/', auth_views.login_user, name='login_user'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mainpage'), name='logout'),
    path('orders/', car_views.order_list, name='order_list'),
    path('orders/create/', car_views.create_order, name='create_order'),
    re_path(r'^orders/(?P<pk>\d+)/$', car_views.order_detail, name='order_detail'),
    path('services/', car_views.services_list, name='services'),
    path('client_orders/', car_views.client_order_list, name='client_order_list'),

    path('crud/', CrudIndex.as_view(), name='crud_index'),

    path('crud/car-types/', CarTypeList.as_view(), name='cartype_list'),
    path('crud/car-types/add/', CarTypeCreate.as_view(), name='cartype_add'),
    path('crud/car-types/<int:pk>/edit/', CarTypeUpdate.as_view(), name='cartype_edit'),
    path('crud/car-types/<int:pk>/delete/', CarTypeDelete.as_view(), name='cartype_delete'),

    path('crud/part-types/', PartTypeList.as_view(), name='parttype_list'),
    path('crud/part-types/add/', PartTypeCreate.as_view(), name='parttype_add'),
    path('crud/part-types/<int:pk>/edit/', PartTypeUpdate.as_view(), name='parttype_edit'),
    path('crud/part-types/<int:pk>/delete/', PartTypeDelete.as_view(), name='parttype_delete'),

    path('crud/parts/', PartList.as_view(), name='part_list'),
    path('crud/parts/add/', PartCreate.as_view(), name='part_add'),
    path('crud/parts/<int:pk>/edit/', PartUpdate.as_view(), name='part_edit'),
    path('crud/parts/<int:pk>/delete/', PartDelete.as_view(), name='part_delete'),


    path('crud/service-types/', ServiceTypeList.as_view(), name='servicetype_list'),
    path('crud/service-types/add/', ServiceTypeCreate.as_view(), name='servicetype_add'),
    path('crud/service-types/<int:pk>/edit/', ServiceTypeUpdate.as_view(), name='servicetype_edit'),
    path('crud/service-types/<int:pk>/delete/', ServiceTypeDelete.as_view(), name='servicetype_delete'),

    path('crud/services-master/', ServiceList.as_view(), name='service_list'),
    path('crud/services-master/add/', service_create, name='service_add'),
    path('crud/services-master/<int:pk>/edit/', service_update, name='service_edit'),
    path('crud/services-master/<int:pk>/delete/', ServiceDelete.as_view(), name='service_delete'),

    path('statistics/', statistics_view, name='statistics'),

    path('reviews/', views.reviews_list, name='reviews_list'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('promo_codes/', views.promo_codes_view, name='promo_codes'),
]