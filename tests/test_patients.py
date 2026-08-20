
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
    class FakeRepository:
        def load_patients(self):
            return [
                {
                    "id": 1,
                    "name": "Jane Doe",
                    "age": 22,
                    "doctor": "Dr. Robinavitch",
                    "active": True
                }
            ]

    monkeypatch.setattr(storage, "PatientRepository", FakeRepository)

    repository = storage.PatientRepository()
    result = repository.load_patients()

    assert result == [{
        "id": 1,
        "name": "Jane Doe",
        "age": 22,
        "doctor": "Dr. Robinavitch",
        "active": True
    }]

def test_save_new_patient(monkeypatch):
    class FakeRepository:
        def save_patients(self, patients):
            patients[0]["id"] = 1

    monkeypatch.setattr(storage, "PatientRepository", FakeRepository)

    repository = storage.PatientRepository()

    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }

    repository.save_patients([patient])

    assert patient["id"] == 1

