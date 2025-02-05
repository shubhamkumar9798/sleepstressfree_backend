import sys
import pickle
import pandas as pd

# Load the Random Forest model from the pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get inputs from the Node.js server via command-line arguments
# print(sys.argv)

# Extract input values from command-line arguments
snoring_rate = float(sys.argv[1])
respiration_rate = float(sys.argv[2])
body_temperature = float(sys.argv[3])
limb_movement = float(sys.argv[4])
blood_oxygen = float(sys.argv[5])
eye_movement = float(sys.argv[6])
sleeping_hours = float(sys.argv[7])
heart_rate = float(sys.argv[8])

# Create a DataFrame for the model input
input_data = pd.DataFrame([[
    snoring_rate,
    respiration_rate,
    body_temperature,
    limb_movement,
    blood_oxygen,
    eye_movement,
    sleeping_hours,
    heart_rate
]], columns=[
    'snoring_rate', 'respiration_rate', 'body_temperature', 
    'limb_movement', 'blood_oxygen', 'eye_movement', 
    'sleeping_hours', 'heart_rate'
])

# Align input_data columns with model's expected columns (feature names during training)
expected_columns = model.feature_names_in_  # Use this to fetch the feature names used during training
# print("Expected columns:", expected_columns)

# Strip any leading/trailing spaces from the expected column names
expected_columns = [col.strip() for col in expected_columns]

# Reorder input_data to match the expected feature order
input_data = input_data[expected_columns]
# print("Input data after reordering:", input_data)

# Make the prediction
prediction = model.predict(input_data)

# Return the prediction (print it so Node.js can capture it)
print(prediction[0])
# print("jlo")