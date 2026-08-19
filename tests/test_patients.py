
import pytest

from patients import validate_patient

import storage


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

def test_load_patients(monkeypatch):
    class FakeCursor:
        def execute(self, query):
            pass

        def fetchall(self):
            return [
                (1, "Jane Doe", 22, "Dr. Robinavitch", 1)
            ]

    monkeypatch.setattr(storage, "cursor", FakeCursor())

    result = storage.load_patients()

    assert result == [{
        "id": 1,
        "name": "Jane Doe",
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": True
    }]

def test_save_new_patient(monkeypatch):
    class FakeCursor:
        def __init__(self):
            self.lastrowid = 1

        def execute(self, query, params=None):
            if query.startswith("SELECT"):
                self.result = None

        def fetchone(self):
            return self.result

    fake_cursor = FakeCursor()
    monkeypatch.setattr(storage, "cursor", fake_cursor)

    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }

    storage.save_patients([patient])

    assert patient["id"] == 1

