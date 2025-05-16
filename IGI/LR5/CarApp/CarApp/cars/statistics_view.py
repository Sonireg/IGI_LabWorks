from django.shortcuts import render
from django.db.models import Avg, Max, Min, Sum, Count
from statistics import mean, median, mode
from django.contrib.admin.views.decorators import staff_member_required
from .models import Client, Order, Service

@staff_member_required
def statistics_view(request):
    # Clients in alphabetical order
    clients = Client.objects.order_by('profile__full_name')
    # Total sales
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total']
    
    # Sales statistics
    sales_amounts = list(Order.objects.values_list('total_price', flat=True))
    sales_avg = mean(sales_amounts) if sales_amounts else 0
    sales_median = median(sales_amounts) if sales_amounts else 0
    sales_mode = mode(sales_amounts) if sales_amounts else 0
    
    # Age statistics
    client_ages = list(Client.objects.values_list('profile__age', flat=True))
    age_avg = mean(client_ages) if client_ages else 0
    age_median = median(client_ages) if client_ages else 0
    
    # Most popular service
    popular_service = Service.objects.annotate(count=Count('order')).order_by('-count').first()
    
    # Most profitable service
    profitable_service = Service.objects.annotate(total_profit=Sum('order__total_price')).order_by('-total_profit').first()
    
    # Data for visualization
    sales_by_date = Order.objects.values('created_at__date').annotate(total=Sum('total_price')).order_by('created_at__date')
    services_distribution = Service.objects.annotate(count=Count('order')).values('name', 'count')
    
    context = {
        'clients': clients,
        'total_sales': total_sales,
        'sales_avg': sales_avg,
        'sales_median': sales_median,
        'sales_mode': sales_mode,
        'age_avg': age_avg,
        'age_median': age_median,
        'popular_service': popular_service,
        'profitable_service': profitable_service,
        'sales_by_date': list(sales_by_date),
        'services_distribution': list(services_distribution),
    }
    return render(request, 'statistics.html', context)
