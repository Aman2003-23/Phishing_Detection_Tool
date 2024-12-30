from flask import Flask, request, jsonify
import joblib

# Load the trained model and vectorizer
model = joblib.load('email_phishing_model.pkl')
vectorizer = joblib.load('email_vectorizer.pkl')

app = Flask(__name__)

@app.route('/predict_email', methods=['POST'])
def predict_email():
    email_text = request.json['email_body']
    
    # Preprocess and vectorize the email body
    email_features = vectorizer.transform([email_text])
    
    # Get prediction
    prediction = model.predict(email_features)[0]
    
    if prediction == 0:
        return jsonify({"prediction": "Legitimate"})
    else:
        return jsonify({"prediction": "Phishing"})

if __name__ == '__main__':
    app.run(debug=True)
