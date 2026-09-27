from storage import PatientRepository

# We keep our repo instance, but the 'patients' global list is COMPLETELY GONE!
patient_repo = PatientRepository()

def validate_patient(patient):
    """Validate a patient record format before allowing it to reach the database."""
    if "id" in patient and not isinstance(patient["id"], int):
        print("Patient ID must be an integer.")
        return False
    
    if not isinstance(patient["name"], str) or not patient["name"].strip():
        print("Patient name must be a valid string.")
        return False
    
    if not isinstance(patient["age"], int) or patient["age"] < 0:
        print("Patient age must be a valid positive integer.")
        return False

    if not isinstance(patient["doctor"], str) or not patient["doctor"].strip():
        print("Doctor name must be a valid string.")
        return False

    if "active" in patient and not isinstance(patient["active"], bool):
        print("Patient status must be a boolean.")
        return False
    
    return True

def show_patient_details(patient):
    """Display the details of a single patient on the screen."""
    print(f"ID: {patient['id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Doctor: {patient['doctor']}")
    print(f"Status: {'Active' if patient['active'] else 'Inactive'}")
    print()

def show_patients(patient_list, counts, status):
    """Display the summary counts and list out all requested patients."""    
    print(f"Total Patient Records: {counts['total']}")
    if status in counts:
        print(f"{status.capitalize()} Patients: {counts[status]}")

    for current_patient in patient_list:
        show_patient_details(current_patient)

def find_patient(patient_id):
    """Finds a patient folder by pulling directly from the DB file."""
    # Bypasses the stale global list and uses our brand-new probe function!
    return patient_repo.get_patient_by_id(patient_id)

def register_patient(name, age, doctor):
    """Registers a new patient and captures the DB-generated ID number."""
    new_patient = {
        "name": name,
        "age": age,
        "doctor": doctor,
        "active": True
    }
    
    # Hand to storage first and catch the counting ID number SQLite generated
    new_id = patient_repo.add_patient(new_patient)
    
    if new_id:
        print(f"Patient {name} (ID: {new_id}) added successfully!")
        return new_id
    else:
        print("Failed to register patient.")
        return None

def update_patient(patient_id, name=None, age=None, doctor=None, active=None):
    """Updates specific patient fields directly via the repository data desk."""
    patient = find_patient(patient_id)
    if patient is None:
        print("Patient not found.")
        return False
        
    if name is not None:
        patient['name'] = name
    if age is not None:
        patient['age'] = age
    if doctor is not None:
        patient['doctor'] = doctor
    if active is not None:
        patient['active'] = active

    return patient_repo.update_patient(patient)

def deactivate_patient(patient_id):
    """Deactivates a patient utilizing our clean, granular update routine."""
    # Reuses your clean update_patient method instead of old bulk dump files!
    success = update_patient(patient_id, active=False)
    if success:
        print(f"Patient {patient_id} deactivated successfully!")
    return success
