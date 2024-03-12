from pydantic import BaseModel


class PredictionDTO(BaseModel):
    prediction: float
