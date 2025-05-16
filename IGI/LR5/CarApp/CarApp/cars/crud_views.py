from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import CarType, PartType, Part, Service, ServiceType
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .forms import ServiceForm, ServicePartFormSet

class CrudIndex(TemplateView):
    template_name = 'crud/index.html'

# CarType CRUD
class CarTypeList(ListView):
    model = CarType
    template_name = 'crud/CarType/car_type_list.html'

class CarTypeCreate(CreateView):
    model = CarType
    fields = ['name', 'description']
    template_name = 'crud/CarType/car_type_form.html'
    success_url = reverse_lazy('cartype_list')

class CarTypeUpdate(UpdateView):
    model = CarType
    fields = ['name', 'description']
    template_name = 'crud/CarType/car_type_form.html'
    success_url = reverse_lazy('cartype_list')

class CarTypeDelete(DeleteView):
    model = CarType
    template_name = 'crud/CarType/car_type_confirm_delete.html'
    success_url = reverse_lazy('cartype_list')

# PartType CRUD
class PartTypeList(ListView):
    model = PartType
    template_name = 'crud/PartType/part_type_list.html'

class PartTypeCreate(CreateView):
    model = PartType
    fields = ['name', 'description']
    template_name = 'crud/PartType//part_type_form.html'
    success_url = reverse_lazy('parttype_list')

class PartTypeUpdate(UpdateView):
    model = PartType
    fields = ['name', 'description']
    template_name = 'crud/PartType//part_type_form.html'
    success_url = reverse_lazy('parttype_list')

class PartTypeDelete(DeleteView):
    model = PartType
    template_name = 'crud/PartType//part_type_confirm_delete.html'
    success_url = reverse_lazy('parttype_list')

# Part CRUD
class PartList(ListView):
    model = Part
    template_name = 'crud/Part/part_list.html'

class PartCreate(CreateView):
    model = Part
    fields = ['part_type', 'name', 'price', 'quantity', 'compatible_car_types']
    template_name = 'crud/Part/part_form.html'
    success_url = reverse_lazy('part_list')

class PartUpdate(UpdateView):
    model = Part
    fields = ['part_type', 'name', 'price', 'quantity', 'compatible_car_types']
    template_name = 'crud/Part/part_form.html'
    success_url = reverse_lazy('part_list')

class PartDelete(DeleteView):
    model = Part
    template_name = 'crud/Part/part_confirm_delete.html'
    success_url = reverse_lazy('part_list')
# ServiceType CRUD
class ServiceTypeList(ListView):
    model = ServiceType
    template_name = 'crud/ServiceType/service_type_list.html'

class ServiceTypeCreate(CreateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'crud/ServiceType/service_type_form.html'
    success_url = reverse_lazy('servicetype_list')

class ServiceTypeUpdate(UpdateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'crud/ServiceType/service_type_form.html'
    success_url = reverse_lazy('servicetype_list')

class ServiceTypeDelete(DeleteView):
    model = ServiceType
    template_name = 'crud/ServiceType/service_type_confirm_delete.html'
    success_url = reverse_lazy('servicetype_list')
# Service CRUD
class ServiceList(ListView):
    model = Service
    template_name = 'crud/Service/service_list.html'

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        formset = ServicePartFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            service = form.save()
            formset.instance = service
            formset.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
        formset = ServicePartFormSet()
    return render(request, 'crud/Service/service_form.html', {'form': form, 'formset': formset})

def service_update(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        formset = ServicePartFormSet(request.POST, instance=service)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
        formset = ServicePartFormSet(instance=service)
    return render(request, 'crud/Service/service_form.html', {'form': form, 'formset': formset})


class ServiceDelete(DeleteView):
    model = Service
    template_name = 'crud/Service/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')
