import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CompanyInfo
from .models import News
from .models import GlossaryEntry
from .models import Master
from .models import Vacancy
from .models import Review
from .models import PromoCode
from .forms import ReviewForm
from django.contrib.auth.models import User
def mainpage(request):
    last_article = News.objects.order_by('-published_at').first() if hasattr(News, 'objects') else None

    jokes = []
    if request.user.is_authenticated:
        for _ in range(3):
            response = requests.get('https://official-joke-api.appspot.com/random_joke')
            if response.status_code == 200:
                joke = response.json()
                query = joke.get('punchline', '')

                # Поиск картинки по шутке
                image_url = None
                if query:
                    headers = {
                        "Authorization": "DXYMhkpFIPBN84eWK680QNKDUwzXbTerQMY1MiNpSXynppFcVJalPMRg"
                    }
                    pexels_resp = requests.get(
                        "https://api.pexels.com/v1/search",
                        headers=headers,
                        params={"query": query, "per_page": 1}
                    )
                    if pexels_resp.status_code == 200:
                        pexels_data = pexels_resp.json()
                        photos = pexels_data.get("photos", [])
                        if photos:
                            image_url = photos[0]["src"]["medium"]

                joke['image_url'] = image_url
                jokes.append(joke)

    
    context = {
        'last_article': last_article,
        'jokes': jokes
    }
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
    return render(request, 'contacts/contacts.html', {'masters': masters})

def policy(request):
    context = {}
    return render(request, 'confidential_policy/confidential_policy.html', context)

def vacancy_list(request):
    vacancies = Vacancy.objects.all()  # Получаем все новости
    return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})

def reviews_list(request):
    reviews = Review.objects.all().order_by('-date')
    return render(request, 'cars/reviews_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = request.user
            review.save()
            return redirect('reviews_list')
    else:
        form = ReviewForm()
    return render(request, 'cars/add_review.html', {'form': form})

def promo_codes_view(request):
    active_promo_codes = PromoCode.objects.filter(is_active=True)
    archived_promo_codes = PromoCode.objects.filter(is_active=False)
    return render(request, 'promo_codes/promo_codes_list.html', {
        'active_promo_codes': active_promo_codes,
        'archived_promo_codes': archived_promo_codes
    })
