from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd
from pydantic import BaseModel

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

# Define request body
class StressPredictionRequest(BaseModel):
    sleep_duration: float
    heart_rate: float
    activity_level: float

@app.post("/predict")
async def predict_stress(data: StressPredictionRequest):
    # Convert input into a NumPy array
    input_data = np.array([[data.sleep_duration, data.heart_rate, data.activity_level]])
    
    # Make a prediction
    prediction = model.predict(input_data)[0]
    
    return {"stress_level": int(prediction)}

