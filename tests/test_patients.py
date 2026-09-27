import pytest
from patients import validate_patient
import storage

@pytest.fixture
def repository(tmp_path):
    """Sets up a clean, isolated temporary database for each test run."""
    db_path = tmp_path / "test.db"
    storage.initialize_database(str(db_path))
    return storage.PatientRepository(str(db_path))


# --- INPUT VALIDATION TESTS ---

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


# --- DATABASE DATA UPDATE TESTS ---

def test_patient_status_change(repository):
    patient = {
        "id": 1,  # ✨ Add an explicit numeric ID here
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

def test_patient_reactivation(repository):
    patient = {
        "id": 1,  # ✨ Add an explicit numeric ID here
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

def test_update_patient_age(repository):
    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }
    repository.add_patient(patient)
    patient["age"] = 40
    repository.update_patient(patient)

    patients_list = repository.get_patients("all")
    updated_patient = patients_list[0]

    assert updated_patient["id"] == patient["id"]
    assert updated_patient["name"] == "Test Patient"
    assert updated_patient["age"] == 40
    assert updated_patient["doctor"] == "Dr. Test"
    assert updated_patient["active"] is True

def test_update_nonexistent_patient(repository):
    patient = {
        "id": 9999,
        "name": "Ghost Patient",
        "age": 50,
        "doctor": "Dr. Test",
        "active": True
    }
    result = repository.update_patient(patient)
    assert result is False

def test_update_patient_name(repository):
    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }
    repository.add_patient(patient)

    patient["name"] = "Updated Patient"
    repository.update_patient(patient)

    patients_list = repository.get_patients("all")
    updated_patient = patients_list[0]

    assert updated_patient["id"] == patient["id"]
    assert updated_patient["name"] == "Updated Patient"
    assert updated_patient["age"] == 30
    assert updated_patient["doctor"] == "Dr. Test"
    assert updated_patient["active"] is True


# --- COMPLIANCE AUDIT HISTORY LOG TESTS ---

def test_patient_registration_creates_activity(repository):
    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }
    repository.add_patient(patient)

    activity = repository.get_patient_activity(patient["id"])

    assert len(activity) == 1
    assert activity[0]["action"] == "Patient registered"

def test_patient_name_update_creates_activity(repository):
    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }
    repository.add_patient(patient)

    patient["name"] = "Updated Patient"
    repository.update_patient(patient)

    activity = repository.get_patient_activity(patient["id"])

    assert len(activity) == 2
    assert activity[1]["action"] == "Name changed"
    assert activity[1]["old_value"] == "Test Patient"
    assert activity[1]["new_value"] == "Updated Patient"

def test_multi_field_update_creates_multiple_activities(repository):
    """Verifies our brand new checks log separate rows when multiple fields change!"""
    patient = {
        "name": "Test Patient",
        "age": 30,
        "doctor": "Dr. Test",
        "active": True
    }
    repository.add_patient(patient)  # Logs entry 1: 'Patient registered'

    # Shift three fields simultaneously to test our new compliance logs
    patient["name"] = "New Name"
    patient["age"] = 35
    patient["doctor"] = "Dr. New"
    repository.update_patient(patient)

    activity = repository.get_patient_activity(patient["id"])

    # Expects 4 rows total: 1 registration + 3 field changes
    assert len(activity) == 4
    
    # Verify our specific action tags are logging beautifully
    actions = [log["action"] for log in activity]
    assert "Name changed" in actions
    assert "Age changed" in actions
    assert "Assigned doctor changed" in actions
