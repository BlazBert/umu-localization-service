from fastapi import FastAPI
from pydantic import BaseModel, RootModel
import pandas as pd
import joblib
import math

def meters_to_lat_lon(origin_lat: float, origin_lon: float,
                      delta_meters_lat: float, delta_meters_lon: float
                     ) -> tuple[float, float]:
    """
    Turn a North-South / East-West offset (in metres) back into
    plain old degrees o’ latitude an’ longitude.
    Good enough fer voyages shorter than ~100 km from the startin’ port.
    """

    R = 6_378_137  # Earth’s radius in metres (same as ye used goin’ forward)

    # Pre-calcs
    origin_lat_rad = math.radians(origin_lat)

    # 1) North-South: metres  →  radians  →  degrees
    delta_lat_deg = math.degrees(delta_meters_lat / R)

    # 2) East-West:  metres  →  radians  →  degrees
    delta_lon_deg = math.degrees(delta_meters_lon / (R * math.cos(origin_lat_rad)))

    # 3) Add the offsets to the point o’ origin
    point_lat = origin_lat + delta_lat_deg
    point_lon = origin_lon + delta_lon_deg

    return point_lat, point_lon



app = FastAPI(title="gNB-UDP API")

# Heave ho – load the model once at launch
model = joblib.load("Random_Forest_model_UDP.pkl")

class Features(RootModel):
    root: dict[str, float]               # 'root' be the lone field

@app.post("/predict")
def predict(features: Features):
    X = pd.DataFrame([features.root])    # note: .root instead o’ __root__
    y_hat = model.predict(X)[0]
    y_lon_lat = meters_to_lat_lon(38.012376667, -1.174046667, #origin_lat, origin_lon are hardcoded and represent the lowest values in the dataset
                      y_hat[0], y_hat[1])
    return {"prediction": y_lon_lat}