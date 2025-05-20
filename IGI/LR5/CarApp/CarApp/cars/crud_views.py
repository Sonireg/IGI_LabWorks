import logging
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import CarType, PartType, Part, Service, ServiceType
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .forms import ServiceForm, ServicePartFormSet
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import News

logger = logging.getLogger(__name__)

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

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

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"CarType created: {self.object}")
        return response

class CarTypeUpdate(UpdateView):
    model = CarType
    fields = ['name', 'description']
    template_name = 'crud/CarType/car_type_form.html'
    success_url = reverse_lazy('cartype_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"CarType updated: {self.object}")
        return response

class CarTypeDelete(DeleteView):
    model = CarType
    template_name = 'crud/CarType/car_type_confirm_delete.html'
    success_url = reverse_lazy('cartype_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug(f"CarType deleted: {obj}")
        return super().delete(request, *args, **kwargs)

# PartType CRUD
class PartTypeList(ListView):
    model = PartType
    template_name = 'crud/PartType/part_type_list.html'

class PartTypeCreate(CreateView):
    model = PartType
    fields = ['name', 'description']
    template_name = 'crud/PartType//part_type_form.html'
    success_url = reverse_lazy('parttype_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"PartType created: {self.object}")
        return response

class PartTypeUpdate(UpdateView):
    model = PartType
    fields = ['name', 'description']
    template_name = 'crud/PartType//part_type_form.html'
    success_url = reverse_lazy('parttype_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"PartType updated: {self.object}")
        return response

class PartTypeDelete(DeleteView):
    model = PartType
    template_name = 'crud/PartType//part_type_confirm_delete.html'
    success_url = reverse_lazy('parttype_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug(f"PartType deleted: {obj}")
        return super().delete(request, *args, **kwargs)

# Part CRUD
class PartList(ListView):
    model = Part
    template_name = 'crud/Part/part_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        part_type = self.request.GET.get('part_type')
        sort_by = self.request.GET.get('sort_by')

        if part_type:
            queryset = queryset.filter(part_type_id=part_type)

        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_types'] = PartType.objects.all()
        return context

class PartCreate(CreateView):
    model = Part
    fields = ['part_type', 'name', 'price', 'quantity', 'compatible_car_types']
    template_name = 'crud/Part/part_form.html'
    success_url = reverse_lazy('part_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"Part created: {self.object}")
        return response

class PartUpdate(UpdateView):
    model = Part
    fields = ['part_type', 'name', 'price', 'quantity', 'compatible_car_types']
    template_name = 'crud/Part/part_form.html'
    success_url = reverse_lazy('part_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"Part updated: {self.object}")
        return response

class PartDelete(DeleteView):
    model = Part
    template_name = 'crud/Part/part_confirm_delete.html'
    success_url = reverse_lazy('part_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug(f"Part deleted: {obj}")
        return super().delete(request, *args, **kwargs)

# ServiceType CRUD
class ServiceTypeList(ListView):
    model = ServiceType
    template_name = 'crud/ServiceType/service_type_list.html'

class ServiceTypeCreate(CreateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'crud/ServiceType/service_type_form.html'
    success_url = reverse_lazy('servicetype_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"ServiceType created: {self.object}")
        return response

class ServiceTypeUpdate(UpdateView):
    model = ServiceType
    fields = ['name', 'description']
    template_name = 'crud/ServiceType/service_type_form.html'
    success_url = reverse_lazy('servicetype_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(f"ServiceType updated: {self.object}")
        return response

class ServiceTypeDelete(DeleteView):
    model = ServiceType
    template_name = 'crud/ServiceType/service_type_confirm_delete.html'
    success_url = reverse_lazy('servicetype_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug(f"ServiceType deleted: {obj}")
        return super().delete(request, *args, **kwargs)

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

# News CRUD
class NewsList(AdminRequiredMixin, ListView):
    model = News
    template_name = 'crud/News/news_list.html'

class NewsCreate(AdminRequiredMixin, CreateView):
    model = News
    fields = ['title', 'content', 'published_date']
    template_name = 'crud/News/news_form.html'
    success_url = reverse_lazy('news_list_admin')

class NewsUpdate(AdminRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'content', 'published_date']
    template_name = 'crud/News/news_form.html'
    success_url = reverse_lazy('news_list_admin')

class NewsDelete(AdminRequiredMixin, DeleteView):
    model = News
    template_name = 'crud/News/news_confirm_delete.html'
    success_url = reverse_lazy('news_list_admin')
