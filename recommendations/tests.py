from django.test import TestCase, Client
from django.urls import reverse
from core.models import Product, Category
from django.core.management import call_command
import json

class RecommendationSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Vegetables')
        self.product1 = Product.objects.create(
            title='Fresh Carrot',
            description='A crunchy and sweet vegetable.',
            category=self.category,
            price=1.50,
            stock_count=100,
            shipping=2
        )
        self.product2 = Product.objects.create(
            title='Organic Broccoli',
            description='A healthy green vegetable.',
            category=self.category,
            price=2.00,
            stock_count=80,
            shipping=2
        )
        self.product3 = Product.objects.create(
            title='Ripe Tomato',
            description='A juicy red vegetable (or fruit?).',
            category=self.category,
            price=1.00,
            stock_count=120,
            shipping=1
        )
        self.product4 = Product.objects.create(
            title='Spinach Bunch',
            description='Fresh green spinach leaves.',
            category=self.category,
            price=3.00,
            stock_count=50,
            shipping=3
        )

        # Build recommendation and price prediction models
        call_command('build_recommendations')
        call_command('train_price_predictor')

    def test_recommend_products(self):
        response = self.client.get(reverse('recommendations:recommend-products', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_search_products(self):
        response = self.client.get(reverse('recommendations:search-products') + '?q=vegetable')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertGreater(len(data), 0)

    def test_predict_price(self):
        response = self.client.get(reverse('recommendations:predict-price') + '?category=Vegetables&stock_count=10&shipping=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('predicted_price', data)
