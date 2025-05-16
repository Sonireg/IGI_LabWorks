from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Order, Service, CarType, Master
from django.forms import inlineformset_factory
from .models import Service, ServicePart, Part
from .validators import validate_phone_number
from django.forms.widgets import TextInput

class ClientRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    email = forms.EmailField(label="Электронная почта")
    age = forms.IntegerField(label="Возраст", min_value=18)
    phone = forms.CharField(
        label="Телефон",
        validators=[validate_phone_number],
        error_messages={'invalid': "Введите корректный номер телефона."},
        widget=TextInput(attrs={
            'type': 'tel',
            'pattern': r'\+?\d{0,15}',
            'oninput': "this.value = this.value.replace(/[^0-9+]/g, '').slice(0, 15);",
            'placeholder': "+1234567890"
        })
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'photo', 'age']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя уже занято. Пожалуйста, выберите другое.")
        return username

    def save(self, commit=True):
        # Сохраняем пользователя
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )

        # Создаём профиль
        profile = super().save(commit=False)
        profile.user = user
        profile.role = 'client'  # Устанавливаем роль клиента

        if commit:
            profile.save()
        return profile

class OrderForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['master', 'car_type', 'services', 'notes']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'name', 'description', 'price', 'duration']

class ServicePartForm(forms.ModelForm):
    class Meta:
        model = ServicePart
        fields = ['part', 'quantity']

ServicePartFormSet = inlineformset_factory(
    Service, ServicePart,
    form=ServicePartForm,
    extra=1,
    can_delete=True
)