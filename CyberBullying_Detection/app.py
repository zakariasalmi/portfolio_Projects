from flask import Flask, render_template, request
import joblib
from sklearn.feature_extraction.text import CountVectorizer

model = joblib.load('modele_naive_bayes.pkl')
vectorizer = joblib.load('vectorizer.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    
    if not text:
        error_message = "Le texte est vide. Veuillez entrer un commentaire."
        return render_template('index.html', error_message=error_message)
    
    transformed_text = vectorizer.transform([text])
    predicted_label = model.predict(transformed_text)[0]
    return render_template('index.html', label=predicted_label, message=text)

if __name__ == "__main__":
    app.run(debug=True)