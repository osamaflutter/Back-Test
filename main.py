from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import time



# Load models
model = joblib.load("model_rf.pkl")
scaler = joblib.load("scaler.pkl")
le_element = joblib.load("le_element.pkl")
le_mix = joblib.load("le_mix.pkl")
le_project = joblib.load("le_project.pkl")

app = FastAPI()

class InputData(BaseModel):
    Element_Type: str
    Mix: str
    Project_Type: str
    Length: float
    Width: float
    Height: float
    Reinforcement_Ratio: float
    Load_Support_Index: float
    Aspect_Ratio: float

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([{
        "Element_Type": le_element.transform([data.Element_Type.strip()])[0],
        "Mix": le_mix.transform([data.Mix.strip()])[0],
        "Project_Type": le_project.transform([data.Project_Type.strip()])[0],
        "Length": data.Length,
        "Width": data.Width,
        "Height": data.Height,
        "Reinforcement Ratio": data.Reinforcement_Ratio,
        "Load_Support_Index": data.Load_Support_Index,
        "Aspect_Ratio": data.Aspect_Ratio
    }])


    df["Volume"] = data.Length * data.Width * data.Height
    df["Steel_Area"] = data.Width * data.Height * data.Reinforcement_Ratio
    df["Support_Pressure"] = data.Load_Support_Index / (data.Length * data.Width + 1e-5)
    df["Slenderness"] = data.Height / (data.Width + 1e-5)
    df["Reinforcement_Density"] = data.Reinforcement_Ratio / (df["Volume"] + 1e-5)

    scaled = scaler.transform(df)
    prediction = model.predict(scaled)
    label = "Safe ✅" if prediction[0] == 1 else "Not Safe ❌"
    return {"prediction": label}
