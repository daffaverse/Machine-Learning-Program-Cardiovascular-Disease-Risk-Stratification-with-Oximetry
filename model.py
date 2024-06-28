from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json

app = Flask(__name__)

# Path ke dataset
dataset_path = 'Dataset.csv'

# Membaca dataset dengan pemisah titik koma
data = pd.read_csv(dataset_path, sep=';')

features = ['Gender / Sex', 'Berat Badan (kg)', 'Tinggi Badan (cm)', 'Detak Jantung (bpm)', 'Kadar Oksigen (%)']
target_health_status = 'Status Kesehatan'  # Perbaikan nama kolom
target_diseases = ['Hipoksemia', 'Tachycardia', 'Bradycardia', 'Pneumonia', 'COPD', 'Asma', 'Gagal Jantung', 'Anemia', 'Sleep Apnea']

# Membagi data menjadi fitur dan target
X = data[features]
y_health_status = data[target_health_status]
y_diseases = data[target_diseases]

# Membagi dataset menjadi data latih dan data uji
X_train, X_test, y_health_status_train, y_health_status_test = train_test_split(X, y_health_status, test_size=0.2, random_state=42)
X_train, X_test, y_diseases_train, y_diseases_test = train_test_split(X, y_diseases, test_size=0.2, random_state=42)

clf_health_status = RandomForestClassifier(random_state=42)
clf_diseases = RandomForestClassifier(random_state=42)

clf_health_status.fit(X_train, y_health_status_train)
clf_diseases.fit(X_train, y_diseases_train)

def predict_health_status_and_diseases(data):
    data = pd.DataFrame([data], columns=features)
    health_status = clf_health_status.predict(data)[0]
    diseases_prob = clf_diseases.predict_proba(data)

    diseases_prob_dict = {}
    for disease, prob in zip(target_diseases, diseases_prob):
        if len(prob[0]) > 1:
            diseases_prob_dict[disease] = prob[0][1] * 100
        else:
            diseases_prob_dict[disease] = prob[0][0] * 100

    return health_status, diseases_prob_dict

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    health_status, diseases_prob_dict = predict_health_status_and_diseases(data)
    response = {
        'Predicted Health Status': health_status,
        'Disease Probabilities': diseases_prob_dict
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
