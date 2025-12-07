import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

from django.core.management.base import BaseCommand
from core.models import Product, Category


class Command(BaseCommand):
    help = 'Train and save a price prediction model'

    def handle(self, *args, **kwargs):
        self.stdout.write('Training price prediction model...')

        # Get all products
        products = Product.objects.all()

        if not products:
            self.stdout.write(self.style.WARNING('No products found in the database.'))
            return

        # Create a dataframe
        df = pd.DataFrame(list(products.values('id', 'price', 'category__title', 'stock_count', 'shipping')))
        df = df.rename(columns={'category__title': 'category'})
        
        # Handle missing values
        df['shipping'] = df['shipping'].fillna(0)
        df['stock_count'] = df['stock_count'].fillna(0)
        df = df.dropna(subset=['price', 'category'])


        # Define features and target
        X = df[['category', 'stock_count', 'shipping']]
        y = df['price']

        # Preprocessing for categorical features
        categorical_features = ['category']
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)],
            remainder='passthrough')
        
        # Create a pipeline
        model = Pipeline(steps=[('preprocessor', preprocessor),
                                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

        # Split data and train the model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        # Save the model and columns
        with open('price_predictor.pkl', 'wb') as f:
            pickle.dump((model, X.columns), f)

        self.stdout.write(self.style.SUCCESS('Successfully trained and saved price prediction model.'))
