
from storage import PatientRepository

patient_repo = PatientRepository()
patients = patient_repo.get_patients("all")

def validate_patient(patient):
    """Validate a patient record."""

    if not isinstance(patient["id"], int):
        print("Patient ID must be an integer.")
        return False
    
    if not isinstance(patient["name"], str):
        print("Patient name must be a string.")
        return False
    
    if not isinstance(patient["age"], int):
        print("Patient age must be an integer.")
        return False

    if not isinstance(patient["doctor"], str):
        print("Doctor name must be a string.")
        return False

    if not isinstance(patient["active"], bool):
        print("Patient status must be a boolean.")
        return False
    
    return True

def show_patient_details(patient):
    """Display the details of a patient."""
    print(f"ID: {patient['id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Doctor: {patient['doctor']}")
    print()

#function that shows all patients
def show_patients(patient_list, counts, status):
    """Display the total number of patients and active patients."""    
    print(f"Total Patient Records: {counts['total']}")

    if status == "active":
        print(f"Active Patients: {counts['active']}")
    elif status == "inactive":
        print(f"Inactive Patients: {counts['inactive']}")

    for current_patient in patient_list:
        show_patient_details(current_patient)

def find_patient(patient_id):
    """Finds patient by ID."""
    for current_patient in patients:
        if current_patient['id'] == patient_id:
            return current_patient
    return None

def register_patient(name, age, doctor):
    """Registers a new patient."""
    new_patient = {
        "name": name,
        "age": age,
        "doctor": doctor,
        "active": True
    }
    patients.append(new_patient)
    patient_repo.add_patient(new_patient)
    print(f"Patient {name} (ID: {new_patient['id']}) added successfully!")

def update_patient(patient_id, name=None, age=None, doctor=None, active=None):
    """Updates patient information."""
    patient = find_patient(patient_id)
    if patient is None:
        return False
    if age is not None:
        patient['age'] = age

    if doctor is not None:
        patient['doctor'] = doctor

    if active is not None:
        patient['active'] = active

    updated = patient_repo.update_patient(patient)

    return updated

def deactivate_patient(patient_id):
    """Deactivates a patient."""
    patient = find_patient(patient_id)
    if patient is None:
        print("Patient not found.")
        return

    patient['active'] = False
    patient_repo.save_patients(patients)
    print(f"Patient {patient_id} deactivated successfully!"     
)