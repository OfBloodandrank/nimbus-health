
import json

import pytest

from patients import validate_patient

from storage import load_patients


def test_valid_patient():
    patient = {
        "id": 12345,
        "name": "Jane Doe",
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": True
    }

    assert validate_patient(patient) == True

def test_invalid_age():
    patient = {
        "id": 12345,
        "name": "Jane Doe",
        "age": "twenty-two",
        "doctor": "Dr. Robinavitch",
        "active": True
    }

    assert validate_patient(patient) == False

def test_invalid_patient_id():
    patient = {
        "id": "12345",
        "name": "Jane Doe",
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": True
    }

    assert validate_patient(patient) == False

def test_invalid_patient_name():
    patient = {
        "id": 12345,
        "name": 12345,
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": True
    }

    assert validate_patient(patient) == False

def test_invalid_doctor_name():
    patient = {
        "id": 12345,
        "name": "Jane Doe",
        "age": 22,
        "doctor": 12345,
        "active": True
    }

    assert validate_patient(patient) == False

def test_invalid_patient_status():
    patient = {
        "id": 12345,
        "name": "Jane Doe",
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": "yes"
    }

    assert validate_patient(patient) == False

def test_load_patients_missing_file(monkeypatch):
    def mock_open(*args, **kwargs):
        raise FileNotFoundError
    monkeypatch.setattr("builtins.open", mock_open)
    result = load_patients()
    assert result == []

def test_load_patients_invalid_json(monkeypatch):
    def mock_json_load(*args, **kwargs):
        raise json.JSONDecodeError("Invalid JSON", "", 0)
    monkeypatch.setattr("json.load", mock_json_load)

    with pytest.raises(SystemExit):
        load_patients()

