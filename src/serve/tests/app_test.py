from fastapi.testclient import TestClient
from src.config import WINDOW_SIZE
from src.serve.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "date" in response.json()
    assert response.json()["status"] == "ok"


def test_fail_predict():
    response = client.post(
        "/mbajk/predict",
        json=[
            {
                "available_bike_stands": 7,
                "surface_pressure": 984.45,
                "temperature": 24.425,
                "apparent_temperature": 23.65,
                "relative_humidity": 43.5
            },
        ],
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == f"Data must contain {WINDOW_SIZE} items"


def test_success_prediction():
    response = client.post(
        "/mbajk/predict",
        json=[
            {
                "available_bike_stands": 7,
                "surface_pressure": 984.45,
                "temperature": 24.425,
                "apparent_temperature": 23.65,
                "relative_humidity": 43.5
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
    response = client.get("/mbajk/stations")
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
    response = client.get("/mbajk/stations/1")
    assert response.status_code == 200
    assert "number" in response.json()
    assert "name" in response.json()
    assert "address" in response.json()
    assert "bike_stands" in response.json()
    assert "available_bike_stands" in response.json()
    assert "available_bikes" in response.json()


def test_predict_multiple():
    response = client.get("/mbajk/predict/3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
    assert "prediction" in response.json()[0]
    assert "date" in response.json()[0]
