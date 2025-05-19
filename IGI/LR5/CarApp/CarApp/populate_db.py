import os
import django
import random
from datetime import timedelta, datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarApp.settings")  # replace with your project settings
django.setup()

from django.contrib.auth.models import User
from cars.models import (
    CarType, ServiceType, PartType, Part, Service, MasterSpecialization,
    Profile, Client, Master, Order, OrderService, ServicePart,
    CompanyInfo, News, GlossaryEntry, Vacancy, Review, PromoCode
)

# Clear existing data (optional)
# Uncomment to delete all existing records
# for model in [OrderService, ServicePart, Order, Service, Part, PartType, ServiceType,
#               CarType, MasterSpecialization, Master, Client, Profile,
#               CompanyInfo, News, GlossaryEntry, Vacancy, Review, PromoCode]:
#     model.objects.all().delete()

# 1. CarType
car_names = ["Sedan", "Hatchback", "SUV", "Coupe", "Convertible", "Wagon", "Minivan", "Pickup", "Crossover", "Van"]
for name in car_names:
    CarType.objects.get_or_create(name=name, defaults={"description": f"Описание для {name}"})

# 2. ServiceType
service_names = ["Oil Change", "Tire Rotation", "Brake Inspection", "Engine Tune-up", "Battery Replacement", "Transmission Check", "Wheel Alignment", "AC Service", "Detailing", "Diagnostics"]
for name in service_names:
    ServiceType.objects.get_or_create(name=name, defaults={"description": f"Описание услуги {name}"})

# 3. PartType
part_type_names = ["Engine", "Brake", "Suspension", "Electrical", "Exhaust", "Cooling", "Fuel", "Transmission", "Steering", "Interior"]
for name in part_type_names:
    PartType.objects.get_or_create(name=name, defaults={"description": f"Тип запчасти {name}"})

# 4. Part
car_types = list(CarType.objects.all())
part_types = list(PartType.objects.all())
for i in range(1, 11):
    pt = random.choice(part_types)
    part, created = Part.objects.get_or_create(
        name=f"{pt.name} Part {i}",
        defaults={
            "part_type": pt,
            "price": round(random.uniform(10, 500), 2),
            "quantity": random.randint(1, 20)
        }
    )
    # assign compatible car types
    part.compatible_car_types.set(random.sample(car_types, k=3))

# 5. Service
service_types = list(ServiceType.objects.all())
parts = list(Part.objects.all())
for i in range(1, 11):
    st = random.choice(service_types)
    svc, created = Service.objects.get_or_create(
        name=f"{st.name} Service {i}",
        defaults={
            "service_type": st,
            "description": f"Описание для услуги {i}",
            "price": round(random.uniform(50, 1000), 2),
            "duration": timedelta(hours=random.randint(1, 5))
        }
    )
    # assign parts through ServicePart
    selected_parts = random.sample(parts, k=3)
    for part in selected_parts:
        ServicePart.objects.get_or_create(service=svc, part=part, defaults={"quantity": random.randint(1, 5)})

# 6. MasterSpecialization
for name in [f"Spec {i}" for i in range(1, 11)]:
    ms, created = MasterSpecialization.objects.get_or_create(name=name)
    ms.service_types.set(random.sample(service_types, k=3))

# 7. Users, Profiles, Clients, Masters
# Create 10 users: 5 masters, 5 clients
for i in range(1, 11):
    username = f"user{i}"
    user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
    user.set_password("password123")
    user.save()
    # Profile
    role = "master" if i <= 5 else "client"
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "role": role,
            "full_name": f"User Fullname {i}",
            "phone": f"+3706000000{i}",
            "age": random.randint(18, 65)
        }
    )
    # Create Client or Master
    if role == "client":
        Client.objects.get_or_create(profile=profile)
    else:
        ms = random.choice(list(MasterSpecialization.objects.all()))
        master, created = Master.objects.get_or_create(
            profile=profile,
            defaults={
                "specialization": ms,
                "experience": random.randint(1, 20)
            }
        )
        master.car_types.set(random.sample(car_types, k=3))

# 8. CompanyInfo
CompanyInfo.objects.get_or_create(title="О компании", defaults={"content": "Информация о компании..."})

# 9. News
for i in range(1, 11):
    News.objects.get_or_create(
        title=f"News Title {i}",
        defaults={
            "content": f"Full content of news {i}.",
            "short_description": f"Short desc {i}.",
            # image omitted
        }
    )

# 10. GlossaryEntry
for term in [f"Term{i}" for i in range(1, 11)]:
    GlossaryEntry.objects.get_or_create(term=term, defaults={"definition": f"Definition for {term}."})

# 11. Vacancy
for i in range(1, 11):
    Vacancy.objects.get_or_create(name=f"Vacancy {i}", defaults={"content": f"Job description {i}."})

# 12. Review
users = list(User.objects.all())
for i in range(1, 11):
    user = random.choice(users)
    Review.objects.get_or_create(
        client=user,
        date=datetime.now(),
        defaults={
            "rating": random.randint(1, 5),
            "text": f"Review text {i}."
        }
    )

# 13. PromoCode
services = list(Service.objects.all())
for i in range(1, 11):
    PromoCode.objects.get_or_create(
        code=f"PROMO{i}",
        defaults={
            "discount": round(random.uniform(5, 50), 2),
            "is_active": True,
            "service": random.choice(services)
        }
    )
# 14. Orders
clients = list(Client.objects.all())
masters = list(Master.objects.all())
services = list(Service.objects.all())
status_choices = [choice[0] for choice in Order.STATUS_CHOICES]

for i in range(1, 21):  # создадим 20 заказов
    client = random.choice(clients)
    master = random.choice(masters)
    car_type = random.choice(car_types)
    selected_services = random.sample(services, k=random.randint(1, 3))

    order = Order.objects.create(
        client=client,
        master=master,
        car_type=car_type,
        status=random.choice(status_choices),
        notes=f"Примечание к заказу {i}"
    )

    total = 0
    for svc in selected_services:
        quantity = random.randint(1, 2)
        OrderService.objects.create(order=order, service=svc, quantity=quantity)
        total += svc.price * quantity

    order.total_price = total
    order.save()


print("Database populated with sample data.")
