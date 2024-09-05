import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Charger le modèle et le vectorizer
with open('models/svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

with open('models/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

def predict_sentiment(text):
    text_vector = vectorizer.transform([text])
    prediction = svm_model.predict(text_vector)
    return prediction[0]
