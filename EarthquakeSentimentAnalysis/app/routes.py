import csv
from flask import Blueprint, request, render_template, jsonify
import pandas as pd
import numpy as np
import pickle

main = Blueprint('main', __name__)

# le modèle SVM et les objets nécessaires
with open('models/svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

with open('models/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

with open('models/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

#  les stopwords en Darija
def load_darija_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        darija_stopwords = set(file.read().splitlines())
    return darija_stopwords

darija_stopwords = load_darija_stopwords('data/darija_stopwords.txt')

import re
from nltk.corpus import stopwords
from camel_tools.utils.normalize import normalize_alef_maksura_ar, normalize_alef_ar, normalize_teh_marbuta_ar

arabic_stopwords = set(stopwords.words('arabic'))

#  nettoyer le texte
def clean_text(text, stopwords):
    text = normalize_alef_maksura_ar(text)
    text = normalize_alef_ar(text)
    text = normalize_teh_marbuta_ar(text)
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    text = re.sub(r'[^ء-ي\s]', '', text)
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

combined_stopwords = arabic_stopwords.union(darija_stopwords)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    cleaned_text = clean_text(text, combined_stopwords)
    text_vectorized = vectorizer.transform([cleaned_text])
    prediction = svm_model.predict(text_vectorized)
    sentiment = label_encoder.inverse_transform(prediction)[0]

    # Enregistrer la prédiction dans un fichier CSV
    df = pd.DataFrame({'text': [text], 'sentiment': [sentiment]})
    df.to_csv('sentiment_predictions.csv', mode='a', header=False, index=False)

    return jsonify({'sentiment': sentiment})

@main.route('/visualize')
def visualize():
    return render_template('visualize.html')

@main.route('/sentiment_data')
def sentiment_data():
    sentiment_counts = {}
    with open('sentiment_predictions.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sentiment = row['sentiment']
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
            else:
                sentiment_counts[sentiment] = 1

    total = sum(sentiment_counts.values())
    sentiment_percentages = {key: value / total for key, value in sentiment_counts.items()}
    return jsonify(sentiment_percentages)





    
    





