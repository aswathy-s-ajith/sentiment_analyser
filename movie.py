# -*- coding: utf-8 -*-
"""movie.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1He1WliZllmDM6dh5YGEseAqfdiysapTD
"""

import matplotlib.pyplot as plt
import os
from imdb import IMDb

def fetch_movie_reviews(movie_name):
    ia = IMDb()
    movie = ia.search_movie(movie_name)

    if movie:
        movie_id = movie[0].movieID
        movie_details = ia.get_movie(movie_id)
        reviews = ia.get_movie_reviews(movie_id)['data']['reviews']
        return [review['content'] for review in reviews]
    else:
        return []

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

def analyze_reviews(reviews):
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for review in reviews:
        score = sid.polarity_scores(review)['compound']
        if score >= 0.05:
            sentiments["Positive"] += 1
        elif score <= -0.05:
            sentiments["Negative"] += 1
        else:
            sentiments["Neutral"] += 1

    return sentiments


def save_bar_graph(sentiment_results):
    labels = list(sentiment_results.keys())
    values = list(sentiment_results.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'red', 'blue'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')

    if not os.path.exists('static'):
        os.makedirs('static')
    plt.savefig('static/sentiment_plot.png')
    plt.close()
