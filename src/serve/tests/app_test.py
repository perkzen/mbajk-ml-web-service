from fastapi.testclient import TestClient
from src.config import WINDOW_SIZE
from src.serve.server import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "date" in response.json()
    assert response.json()["status"] == "ok"


def test_fail_predict():
    response = client.post(
        "/mbjak/predict",
        json=[
            {
                "available_bike_stands": 10,
                "available_bikes": 5,
                "temperature": 20.0,
                "relative_humidity": 50.0,
                "dew_point": 10.0,
                "apparent_temperature": 20.0,
                "precipitation": 0.0,
                "rain": 0.0,
                "surface_pressure": 1000.0,
            }
        ],
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Data must contain 50 items"


def test_success_prediction():
    response = client.post(
        "/mbjak/predict",
        json=[
            {
                "available_bike_stands": 10,
                "available_bikes": 5,
                "temperature": 20.0,
                "relative_humidity": 50.0,
                "dew_point": 10.0,
                "apparent_temperature": 20.0,
                "precipitation": 0.0,
                "rain": 0.0,
                "surface_pressure": 1000.0,
            }
            for _ in range(WINDOW_SIZE)
        ],
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], int)
    assert response.json()["prediction"] >= 0
    assert response.json()["prediction"] <= 100
