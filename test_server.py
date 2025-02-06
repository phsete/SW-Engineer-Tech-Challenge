import pytest
from fastapi.testclient import TestClient
from server import app, init_db
import models
import sqlite3
from unittest import mock
import os

def clear_db(test_db_filename = "test_series_data.db"):
    try:
        os.remove(test_db_filename) # Remove Test DB file if it was somehow not deleted earlier
    except OSError:
        pass

@pytest.fixture
def client():
    test_db_filename = "test_series_data.db"
    clear_db(test_db_filename)
    # Use test database to not influence potential real database
    with mock.patch("server.connect_to_db", lambda name="": sqlite3.connect(test_db_filename)):
        client = TestClient(app)
        yield client
    clear_db(test_db_filename)
    

@pytest.fixture
def test_series():
    # Test data with updated values
    return models.Series(
        SeriesInstanceUID="1.23.456.7890",
        PatientName="Firstname^Lastname",
        PatientID=42,
        StudyInstanceUID="0.98.765.4321",
        InstancesInSeries=25
    )

def test_add_series(client, test_series):
    # Test successful insertion
    response = client.post("/series", json=test_series.model_dump())
    
    assert response.status_code == 201  # Created
    assert response.json() == test_series.model_dump()

    # Verify the data was inserted into the DB
    cur, con = init_db()
    res = cur.execute("SELECT * FROM series_data WHERE SeriesInstanceUID = '1.23.456.7890'")
    row = res.fetchone()
    assert row is not None
    assert row[1] == "Firstname^Lastname"  # PatientName
    assert row[2] == 42                   # PatientID
    assert row[3] == "0.98.765.4321"      # StudyInstanceUID
    assert row[4] == 25                   # InstancesInSeries
    con.close()

def test_add_duplicate_series(client, test_series):
    # Test if a duplicate entry causes a 403 repsonse
    response = client.post("/series", json=test_series.model_dump())
    assert response.status_code == 403  # Forbidden
    assert response.json() == {}

def test_invalid_series_data(client):
    # Test handling of invalid data (missing required fields, etc.)
    invalid_data = {
        "SeriesInstanceUID": "1.23.456.7890",
        "PatientName": "Firstname^Lastname",
        # Missing PatientID, StudyInstanceUID, InstancesInSeries
    }
    response = client.post("/series", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity