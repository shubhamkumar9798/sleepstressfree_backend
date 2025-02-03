from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load the model
if os.path.exists('model.pkl'):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
else:
    model = None

# Endpoint for predictions
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model is not available for prediction."}), 500

    try:
        # Get input data from the request (JSON)
        data = request.json

        # Extract features from the JSON request
        features = np.array([[
            data['snoring_rate'],
            data['respiration_rate'],
            data['body_temperature'],
            data['limb_movement'],
            data['blood_oxygen'],
            data['eye_movement'],
            data['sleeping_hours'],
            data['heart_rate']
        ]])

        # Predict the stress level
        prediction = model.predict(features)[0]

        # Save the new data back to the CSV to grow the dataset
        new_data = pd.DataFrame([data])
        new_data['stress_level'] = prediction
        new_data.to_csv('sleep_data.csv', mode='a', header=False, index=False)

        return jsonify({"stress_level": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
