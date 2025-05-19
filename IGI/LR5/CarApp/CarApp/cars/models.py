from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Типы автомобилей
class CarType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = [
        ('master', 'Мастер'),
        ('client', 'Клиент'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Связываем с базовой моделью User
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="master")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, default='placeholder.png')
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(MinValueValidator(18), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def get_image_url(self):
        return self.photo.url if self.photo else 'placeholder.png'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
# Типы услуг
class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления    
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.name

# Виды запчастей
class PartType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.name

# Запчасти
class Part(models.Model):
    part_type = models.ForeignKey(PartType, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0)
    compatible_car_types = models.ManyToManyField(CarType)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления

    def __str__(self):
        return f"{self.name} ({self.part_type.name})"

# Услуги
class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.DurationField()
    parts = models.ManyToManyField(Part, through='ServicePart')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return f"{self.name} - {self.price} руб."

# Специализации мастеров
class MasterSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    service_types = models.ManyToManyField(ServiceType)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.name

# Клиенты
class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='client', blank=True, null=True) 
    def __str__(self):
        return self.profile.full_name

# Мастера
class Master(models.Model):
    specialization = models.ForeignKey(MasterSpecialization, on_delete=models.PROTECT)
    experience = models.PositiveIntegerField(default=0)
    car_types = models.ManyToManyField(CarType)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='master', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления

    def __str__(self):
        return f"{self.profile.full_name} ({self.specialization.name})"

# Заказы
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True)
    car_type = models.ForeignKey(CarType, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Removed duplicate field
    updated_at = models.DateTimeField(auto_now=True)      # Removed duplicate field
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    services = models.ManyToManyField(Service, through='OrderService')
    def __str__(self):
        return f"Заказ #{self.id} - {self.client.profile.full_name} ({self.status})"

# Промежуточная модель для услуг в заказе
class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    class Meta:
        unique_together = ('order', 'service')

# Промежуточная модель для запчастей в заказе

class ServicePart(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # <- исправлено
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    class Meta:
        unique_together = ('service', 'part')  # <- исправлено

class CompanyInfo(models.Model):
    title = models.CharField(max_length=200, default='О компании')
    content = models.TextField()

    def __str__(self):
        return self.title
    
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    short_description = models.CharField(max_length=255)  # Краткое содержание
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, default='placeholder.png')  # Картинка
    published_at = models.DateTimeField(auto_now_add=True)  # Дата публикации
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.title

    def get_image_url(self):
        return self.image.url if self.image else 'placeholder.png'
    
class GlossaryEntry(models.Model):
    term = models.CharField(max_length=200, unique=True, verbose_name="Термин")
    definition = models.TextField(verbose_name="Определение")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата добавления", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.term
    
class Vacancy(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Время добавления
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Время обновления
    def __str__(self):
        return self.name

class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} - {self.rating} stars"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка (%)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.code} - {'Активен' if self.is_active else 'Архив'}"