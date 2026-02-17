from fastapi import APIRouter
from pydantic import BaseModel
from ml_service.ml.predictor import predict_price

router = APIRouter()


class PriceRequest(BaseModel):
    classification: str
    avg_local_ward_class_knn_10: float
    dist_highway_m: float
    dist_main_road_m: float
    dist_inner_road_m: float
    dist_nearest_infra_m: float
    latitude: float
    longitude: float


@router.post("/predict-price")
def get_price(request: PriceRequest):
    input_data = request.dict()
    price = predict_price(input_data)

    return {
        "predicted_price_per_sq_yard": price
    }
