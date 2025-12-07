import pickle
from django.http import JsonResponse
from core.models import Product, Category
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.urls import reverse
import requests


def demo(request):
    # Get a product for recommendations
    product_for_recommendation = Product.objects.first()
    if not product_for_recommendation:
        return render(request, 'recommendations/demo.html', {'error': 'No products in the database.'})

    # Get a category for search
    category = Category.objects.first()
    search_query = category.title if category else "product"
        
    # Get recommendations
    recommend_url = request.build_absolute_uri(reverse('recommendations:recommend-products', args=[product_for_recommendation.id]))
    recommend_response = requests.get(recommend_url)
    recommendations = recommend_response.json() if recommend_response.status_code == 200 else []

    # Search for products
    search_url = request.build_absolute_uri(reverse('recommendations:search-products')) + f'?q={search_query}'
    search_response = requests.get(search_url)
    search_results = search_response.json() if search_response.status_code == 200 else []

    # Predict price
    predict_url = request.build_absolute_uri(reverse('recommendations:predict-price')) + f'?category={search_query}&stock_count=10&shipping=10'
    predict_response = requests.get(predict_url)
    predicted_price = predict_response.json() if predict_response.status_code == 200 else {}

    context = {
        'product_for_recommendation': product_for_recommendation,
        'recommendations': recommendations,
        'search_query': search_query,
        'search_results': search_results,
        'prediction_input': {'category': search_query, 'stock_count': 10, 'shipping': 10},
        'predicted_price': predicted_price.get('predicted_price'),
    }
    return render(request, 'recommendations/demo.html', context)


def recommend_products(request, product_id):
    try:
        with open('recommendations.pkl', 'rb') as f:
            df, cosine_sim, tfidf = pickle.load(f)
    except FileNotFoundError:
        return JsonResponse({'error': 'Recommendations have not been built yet.'}, status=500)

    if product_id not in df['id'].values:
        return JsonResponse({'error': 'Product not found.'}, status=404)

    idx = df[df['id'] == product_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    product_indices = [i[0] for i in sim_scores]
    
    recommended_products = df.iloc[product_indices]
    
    # recommended_products_json = recommended_products.to_json(orient='records')
    
    recommended_products_data = []
    for index, row in recommended_products.iterrows():
        product = Product.objects.get(id=row['id'])
        recommended_products_data.append({
            'id': product.id,
            'title': product.title,
            'product_image': product.image.url if product.image else None,
            'price': product.price,

        })


    return JsonResponse(recommended_products_data, safe=False)


def search_products(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'error': 'Please provide a search query.'}, status=400)

    try:
        with open('recommendations.pkl', 'rb') as f:
            df, cosine_sim, tfidf = pickle.load(f)
    except FileNotFoundError:
        return JsonResponse({'error': 'Search index has not been built yet.'}, status=500)

    query_vec = tfidf.transform([query])
    results = cosine_similarity(query_vec, tfidf.fit_transform(df['title'] + ' ' + df['description'])).flatten()
    
    # Get top 5 results
    top_5_indices = results.argsort()[-5:][::-1]
    
    product_indices = [i for i in top_5_indices]
    
    searched_products = df.iloc[product_indices]
    
    searched_products_data = []
    for index, row in searched_products.iterrows():
        product = Product.objects.get(id=row['id'])
        searched_products_data.append({
            'id': product.id,
            'title': product.title,
            'product_image': product.image.url if product.image else None,
            'price': product.price,

        })
        
    return JsonResponse(searched_products_data, safe=False)


def predict_price(request):
    category = request.GET.get('category')
    stock_count = request.GET.get('stock_count')
    shipping = request.GET.get('shipping')

    if not all([category, stock_count, shipping]):
        return JsonResponse({'error': 'Please provide all the required attributes: category, stock_count, shipping.'}, status=400)

    try:
        with open('price_predictor.pkl', 'rb') as f:
            model, columns = pickle.load(f)
    except FileNotFoundError:
        return JsonResponse({'error': 'Price predictor has not been trained yet.'}, status=500)

    try:
        stock_count = int(stock_count)
        shipping = float(shipping)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid data type for stock_count or shipping.'}, status=400)

    data = pd.DataFrame([[category, stock_count, shipping]], columns=columns)

    predicted_price = model.predict(data)[0]

    return JsonResponse({'predicted_price': predicted_price})
