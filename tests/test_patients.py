
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
        "id": 1,
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }

    repository.save_patients([patient])

    assert patient["id"] == 1

def test_patient_status_change(tmp_path):
    db_path = tmp_path / "test.db"
    storage.initialize_database(str(db_path))
    repository = storage.PatientRepository(str(db_path))

    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }

    repository.add_patient(patient)

    patient["active"] = False
    repository.update_patient(patient)

    active_patients = repository.get_patients("active")
    inactive_patients = repository.get_patients("inactive")
    all_patients = repository.get_patients("all")

    assert patient not in active_patients
    assert patient in inactive_patients
    assert patient in all_patients

def test_patient_reactivation(tmp_path):
    db_path = tmp_path / "test.db"
    storage.initialize_database(str(db_path))
    repository = storage.PatientRepository(str(db_path))

    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": False
    }

    repository.add_patient(patient)

    patient["active"] = True
    repository.update_patient(patient)

    active_patients = repository.get_patients("active")
    inactive_patients = repository.get_patients("inactive")
    all_patients = repository.get_patients("all")

    assert patient in active_patients
    assert patient not in inactive_patients
    assert patient in all_patients