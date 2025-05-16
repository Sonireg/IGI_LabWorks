
from .models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Profile, Client, Order, Service

@login_required
def order_list(request):
    
    profile = request.user.profile
    if profile.role != 'master':
        return render(request, 'cars/orders/not_allowed.html')  # если не клиент

    orders = Order.objects.filter(master__profile=profile).select_related('car_type', 'master__profile')
    context = {'orders': orders}
    context["total_price"] = sum([order.total_price for order in orders])
    return render(request, 'cars/orders/order_list.html', context)

@login_required
def client_order_list(request):
    profile = request.user.profile
    if profile.role != 'client':
        return render(request, 'cars/orders/not_allowed.html')  # если не клиент

    orders = Order.objects.filter(client__profile=profile).select_related('car_type', 'master__profile')
    return render(request, 'cars/orders/order_list.html', {'orders': orders})

@login_required
def create_order(request):
    try:
        client = request.user.profile.client
    except:
        return redirect('mainpage')  # если не клиент – назад

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.total_price = sum(service.price for service in form.cleaned_data['services'])  # автосумма
            order.save()
            form.save_m2m()  # сохранить M2M
            return redirect('client_order_list')  # например, на страницу со списком заказов клиента
    else:
        form = OrderForm()

    return render(request, 'cars/orders/create_order.html', {'form': form})

def services_list(request):
    services = Service.objects.all().select_related('service_type')
    context = {'services': services}
    return render(request, 'cars/services.html', context)

