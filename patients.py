import json

from storage import load_patients, save_patients

#function that validates patient data types
def validate_patient(patient):

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

#show patient details function
def show_patient_details(patient):
    print(f"ID: {patient['id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Doctor: {patient['doctor']}")
    print()

#function that shows all patients
def show_patients():

    total_patients = len(patients)
    active_patients = sum(patient["active"] for patient in patients)
    print (f"Total Patient Records: {total_patients}") 
    print (f"Active Patients: {active_patients}")
    print()

    for current_patient in patients:
        if current_patient['active']:
            show_patient_details(current_patient)


#function that finds a patient by ID

def find_patient(patient_id):
    for current_patient in patients:
        if current_patient['id'] == patient_id:
            return current_patient
    return None

#function that registers a new patient

def register_patient(name, age, doctor):
    biggest_id = max(patient['id'] for patient in patients)
    new_id = biggest_id + 1
    new_patient = {
        "id": new_id,
        "name": name,
        "age": age,
        "doctor": doctor,
        "active": True
    }
    patients.append(new_patient)
    save_patients()
    print(f"Patient {name} (ID: {new_id}) added successfully!")

#function that updates patient information
def update_patient(patient_id, name=None, age=None, doctor=None):
    patient = find_patient(patient_id)
    if name is not None:
        patient['name'] = name
    if age is not None:
        patient['age'] = age

    if doctor is not None:
        patient['doctor'] = doctor
    save_patients()
    print(f"Patient {patient_id} updated successfully!")

#function that deactivates a patient
def deactivate_patient(patient_id):
    patient = find_patient(patient_id)
    if patient is None:
        print("Patient not found.")
        return

    patient['active'] = False
    save_patients()
    print(f"Patient {patient_id} deactivated successfully!")