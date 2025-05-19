from django.contrib import admin
from .models import (
    CarType, Client, ServiceType, MasterSpecialization,
    Master, PartType, Part, Service,
    Order, OrderService, ServicePart, 
    CompanyInfo, News, GlossaryEntry, Profile, 
    Vacancy, Review, PromoCode
)
# Register your models here.
admin.site.register(CarType)
admin.site.register(Client)
admin.site.register(ServiceType)
admin.site.register(MasterSpecialization)
admin.site.register(Master)
admin.site.register(PartType)
admin.site.register(Part)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderService)
admin.site.register(ServicePart)
admin.site.register(CompanyInfo)
admin.site.register(News)
admin.site.register(GlossaryEntry)
admin.site.register(Profile)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)