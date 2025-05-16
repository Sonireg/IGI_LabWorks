import requests
from django.shortcuts import render
from .models import CompanyInfo
from .models import News
from .models import GlossaryEntry
from .models import Master
from .models import Vacancy

def index(request):
    context = {}
    return render(request, 'weather/index.html', context)


def mainpage(request):
    last_article = None
    if hasattr(News, 'objects'):
        last_article = News.objects.order_by('-published_at').first()
    context = {'last_article': last_article}
    return render(request, 'mainpage/mainpage.html', context)

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'about/about.html', {'company_info': company_info})

def news_list(request):
    news_items = News.objects.all()  # Получаем все новости
    return render(request, 'news/news_list.html', {'news_items': news_items})

def news_detail(request, pk):
    article = News.objects.get(pk=pk)  # Получаем статью по её идентификатору
    print(article)
    return render(request, 'news/news_detail.html', {'news': article})

def glossary_view(request):
    entries = GlossaryEntry.objects.order_by('-created_at')
    return render(request, 'glossary/glossary_list.html', {'entries': entries})


def contacts_view(request):
    # Извлекаем всех мастеров с их профилями
    masters = Master.objects.select_related('profile').all()
    print(masters)
    return render(request, 'contacts/contacts.html', {'masters': masters})

def policy(request):
    context = {}
    return render(request, 'confidential_policy/confidential_policy.html', context)

def vacancy_list(request):
    vacancies = Vacancy.objects.all()  # Получаем все новости
    return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})
