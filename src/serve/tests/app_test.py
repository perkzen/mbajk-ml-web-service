from fastapi.testclient import TestClient
from src.config import WINDOW_SIZE
from src.serve.main import app

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


def test_get_bike_stations():
    response = client.get("/mbjak/stations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "number" in response.json()[0]
    assert "name" in response.json()[0]
    assert "address" in response.json()[0]
    assert "bike_stands" in response.json()[0]
    assert "available_bike_stands" in response.json()[0]
    assert "available_bikes" in response.json()[0]


def test_get_bike_station_by_number():
    response = client.get("/mbjak/stations/1")
    assert response.status_code == 200
    assert "number" in response.json()
    assert "name" in response.json()
    assert "address" in response.json()
    assert "bike_stands" in response.json()
    assert "available_bike_stands" in response.json()
    assert "available_bikes" in response.json()
