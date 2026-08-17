import json

def load_patients():
    """Load patient records from the JSON file."""
    try:
        with open("patients.json", "r") as file:
            patients = json.load(file)
            return patients
                 
    except FileNotFoundError:
        print("Patient data file not found.")
        return []
    except json.JSONDecodeError:
        print("Patient data file contains invalid JSON.")
        exit()


def save_patients(patients):
    """Save patient records to the JSON file."""
    with open("patients.json", "w") as file:
        json.dump(patients, file, indent=4)