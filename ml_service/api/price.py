from fastapi import APIRouter
from pydantic import BaseModel
from ml_service.ml.predictor import predict_price
from ml_service.features.spatial_engine import spatial_engine

router = APIRouter()


class PriceRequest(BaseModel):
    classification: str
    latitude: float
    longitude: float


@router.post("/predict-price")
def predict(request: PriceRequest):

    # Step 1: Compute spatial features
    features = spatial_engine.compute_features(
        request.latitude,
        request.longitude
    )

    # Step 2: Merge everything
    model_input = {
        "classification": request.classification,
        "latitude": request.latitude,
        "longitude": request.longitude,
        **features
    }

    # Step 3: Predict
    price = predict_price(model_input)

    return {
        "predicted_price_per_sq_yard": price ,
        "features_used": features
    }
