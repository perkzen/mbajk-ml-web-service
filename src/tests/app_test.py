from fastapi.testclient import TestClient
from src.serve.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "date" in response.json()
    assert response.json()["status"] == "ok"


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


def test_fail_predict_multiple():
    response = client.get("/mbajk/predict/1/0")
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "n_future must be greater than 0"


def test_fail_predict_multiple_2():
    response = client.get("/mbajk/predict/30/1")
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "station_number must be between 0 and 28"


def test_predict_multiple():
    response = client.get("/mbajk/predict/1/3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
    assert "prediction" in response.json()[0]
    assert "date" in response.json()[0]
