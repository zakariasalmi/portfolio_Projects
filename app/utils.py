from flask import Blueprint, render_template, request, jsonify
import pickle
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
arabic_stopwords = set(stopwords.words('arabic'))

# Charger les stopwords en Darija à partir du fichier
def load_darija_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        darija_stopwords = set(file.read().splitlines())
    return darija_stopwords

# Fonction pour nettoyer le texte
def clean_text(text, stopwords):
    # Supprimer les diacritiques
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    # Supprimer les caractères non arabes (y compris les chiffres et la ponctuation)
    text = re.sub(r'[^ء-ي\s]', '', text)
    # Supprimer les mots d'arrêt
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

main = Blueprint('main', __name__)

# Charger le modèle SVM
with open('models/svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

# Charger le label encoder
with open('models/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

# Charger le vectorizer
with open('models/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Charger les stopwords en Darija
darija_stopwords = load_darija_stopwords('darija_stopwords.txt')

# Combiner les deux listes de stopwords
combined_stopwords = arabic_stopwords.union(darija_stopwords)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    # Prétraitement et vectorisation du texte
    cleaned_text = clean_text(text, combined_stopwords)
    text_vectorized = vectorizer.transform([cleaned_text])
    prediction = svm_model.predict(text_vectorized)
    sentiment = label_encoder.inverse_transform(prediction)[0]
    return jsonify({'sentiment': sentiment})
