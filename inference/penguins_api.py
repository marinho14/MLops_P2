import joblib
import sklearn
from fastapi import FastAPI, HTTPException , APIRouter
import uvicorn
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

class Penguin(BaseModel):
    studyName: List[str] = ['PAL0708']
    sampleNumber: List[int] = [1]
    region: List[str] = ['Anvers']
    island: List[str] = ['Torgersen']
    stage: List[str] = ['Adult, 1 Egg Stage']
    individualID: List[str] = ['N1A1']
    clutchCompletion: List[str] = ['Yes']
    dateEgg: List[str] = ['11/11/07']
    culmenLen: List[float] = [39.1]
    culmenDepth: List[float] = [18.7]
    flipperLen: List[int] = [181]
    bodyMass: List[int] = [3750]
    sex: List[str] = ['MALE']
    delta15N: List[float] = [0.0]
    delta13C: List[float] = [0.0]
    comments: List[str] = ['Not enough blood for isotopes.'] 

species_mapping = {'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2}

app = FastAPI()
    
def decode_input(input):
    sex_label_encoder = joblib.load('/opt/airflow/encoders/sex_label_encoder.pkl')
    input_dict=dict(input)
    df = pd.DataFrame.from_dict(input_dict)
    df['sex'] = sex_label_encoder.transform(df['sex'].astype("string"))
    model_columns = ['culmenLen', 'culmenDepth', 'flipperLen', 'bodyMass', 'sex', 'delta15N', 'delta13C']
    df = df[model_columns]
    print(df)
    return df
    

@app.post("/predict/{model_name}")
def predict_model(model_name: str, input_data : Penguin):
    # Cargar el modelo según el nombre proporcionado
    model_path = f"/opt/airflow/models/{model_name}.pkl"
    model = joblib.load(model_path)

    # Decodificar los datos de entrada
    decoded_input = decode_input(input_data)
    print(decoded_input)
    prediction = model.predict(decoded_input)
    prediction_list = prediction.tolist()
    prediction_mapped = [list(species_mapping.keys())[list(species_mapping.values()).index(x)] for x in prediction_list]
    
    return {"model_used": model_name, "prediction":prediction_mapped}

@app.get("/get_models")
def get_models():
    dir_list = os.listdir("/opt/airflow/models/")
    models_avaible = [elemento.split(".")[0] for elemento in dir_list]
    return models_avaible