import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarApp.settings')

from django.test import TestCase, Client
from django.urls import reverse
from .models import News, CompanyInfo, GlossaryEntry, Master, Vacancy, Review, PromoCode
from django.contrib.auth.models import User
import pytest

class MainPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.news = News.objects.create(title="Test News", content="Test Content")

    def test_mainpage_view(self):
        response = self.client.get(reverse('mainpage'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('last_article', response.context)

class AboutPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        CompanyInfo.objects.create(title="Test Company", content="Test Description")  # Fixed field names

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('company_info', response.context)

class GlossaryTests(TestCase):
    def setUp(self):
        self.client = Client()
        GlossaryEntry.objects.create(term="Test Term", definition="Test Definition")

    def test_glossary_view(self):
        response = self.client.get(reverse('glossary'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('entries', response.context)

class VacancyTests(TestCase):
    def setUp(self):
        self.client = Client()
        Vacancy.objects.create(name="Test Vacancy", content="Test Description")  # Fixed field names

    def test_vacancy_list_view(self):
        response = self.client.get(reverse('career'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('vacancies', response.context)

class PromoCodeTests(TestCase):
    def setUp(self):
        self.client = Client()
        PromoCode.objects.create(code="TESTCODE", discount=10.0, is_active=True)  # Added discount value

    def test_promo_codes_view(self):
        response = self.client.get(reverse('promo_codes'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('active_promo_codes', response.context)

@pytest.mark.parametrize("url_name,expected_status", [
    ('mainpage', 200),
    ('about', 200),
    ('glossary', 200),
    ('career', 200),
    ('promo_codes', 200),
])
def test_views_status_code(client, url_name, expected_status):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == expected_status
