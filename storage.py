import json

# Load patients from the JSON file
def load_patients():
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

patients = load_patients()


# Save patients to the JSON file
def save_patients():
    with open("patients.json", "w") as file:
        json.dump(patients, file, indent=4)