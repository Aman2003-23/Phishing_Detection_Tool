from flask import Flask, request, jsonify
import joblib

# Load the trained model and vectorizer
model = joblib.load('url_phishing_model.pkl')
vectorizer = joblib.load('url_vectorizer.pkl')

app = Flask(__name__)

# Route to handle the prediction for URLs
@app.route('/predict_url', methods=['POST'])
def predict_url():
    # Get the URL from the POST request
    data = request.json
    url = data.get('url')  # Get the URL from the request data
    
    # If the URL is not in the request, return an error
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Vectorize the URL using the same vectorizer used for training
    url_features = vectorizer.transform([url])
    
    # Predict using the trained model
    prediction = model.predict(url_features)[0]
    
    # Map the prediction to the corresponding result
    result = "Malicious URL" if prediction == 1 else "Legitimate URL"
    
    # Return the result
    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)
