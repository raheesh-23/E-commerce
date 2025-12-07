import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Build and save TF-IDF and cosine similarity matrices for product recommendations'

    def handle(self, *args, **kwargs):
        self.stdout.write('Building recommendation matrices...')

        # Get all products
        products = Product.objects.all()

        if not products:
            self.stdout.write(self.style.WARNING('No products found in the database.'))
            return

        # Create a dataframe
        df = pd.DataFrame(list(products.values('id', 'title', 'description')))
        df['description'] = df['description'].fillna('')

        # Create a TF-IDF vectorizer
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['title'] + ' ' + df['description'])

        # Calculate cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Save the matrices and the dataframe
        with open('recommendations.pkl', 'wb') as f:
            pickle.dump((df, cosine_sim, tfidf), f)

        self.stdout.write(self.style.SUCCESS('Successfully built and saved recommendation matrices.'))
