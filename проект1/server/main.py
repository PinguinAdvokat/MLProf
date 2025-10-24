import pickle
import sklearn
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Model_router():
    def __init__(self):
        self.models = {}
        for filename in os.listdir("models"):
            filepath = os.path.join("models", filename)
            with open(filepath, "rb") as f:
                model = pickle.load(f)
                self.models.update({filename.replace(".bytes", ""): model})

    def predict(self, target:str, X):
        if target not in self.models:
            raise ValueError(f"model for solve {target} not found")
        return self.models[target].predict(X)


class Characteristics(BaseModel):
    weight: float
    calories: float

class SessionStatistics(BaseModel):
    expected_burn: float
    workout_frequency: float
    Session_Duration: float


app = FastAPI()
model = Model_router()


@app.put("/predict/lean_mass_kg")
async def predict(chars: Characteristics):
    ans = model.predict("lean_mass_kg", [[chars.weight, chars.calories]])
    return ans.tolist()


@app.put("/predict/experience_level")
async def predict(stats: SessionStatistics):
    ans = model.predict("experience_level", [[stats.expected_burn, stats.workout_frequency, stats.Session_Duration]])
    return ans.tolist()