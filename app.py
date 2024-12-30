from flask import Flask, request, jsonify
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained models and vectorizers
url_model = joblib.load('url_phishing_model.pkl')  # Trained URL phishing model
url_vectorizer = joblib.load('url_vectorizer.pkl')  # URL vectorizer

email_model = joblib.load('email_phishing_model.pkl')  # Trained email phishing model
email_vectorizer = joblib.load('email_vectorizer.pkl')  # Email vectorizer

app = Flask(__name__)

# Route for URL phishing prediction
@app.route('/predict_url', methods=['POST'])
def predict_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Vectorize the URL
    url_features = url_vectorizer.transform([url])
    
    # Predict using the URL phishing model
    url_prediction = url_model.predict(url_features)[0]
    
    # Map the prediction to the corresponding result
    url_result = "Malicious URL" if url_prediction == 1 else "Legitimate URL"
    
    return jsonify({"prediction": url_result})

# Route for email phishing prediction
@app.route('/predict_email', methods=['POST'])
def predict_email():
    data = request.json
    email_text = data.get('email_text')
    
    if not email_text:
        return jsonify({"error": "Email text is required"}), 400
    
    # Vectorize the email text
    email_features = email_vectorizer.transform([email_text])
    
    # Predict using the email phishing model
    email_prediction = email_model.predict(email_features)[0]
    
    # Map the prediction to the corresponding result
    email_result = "Malicious Email" if email_prediction == 1 else "Legitimate Email"
    
    return jsonify({"prediction": email_result})

if __name__ == '__main__':
    app.run(debug=True)
