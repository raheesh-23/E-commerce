from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path('recommend/<int:product_id>/', views.recommend_products, name='recommend-products'),
    path('search/', views.search_products, name='search-products'),
    path('predict-price/', views.predict_price, name='predict-price'),
    path('demo/', views.demo, name='demo'),
]
