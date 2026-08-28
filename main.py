from storage import PatientRepository
import patients
patient_repo = PatientRepository()

# Main program loop
while True:
    print("1. View Active Patients")
    print("2. View Inactive Patients")
    print("3. View All Patients")
    print("4. Register Patient")
    print("5. Search for a Patient")
    print("6. Update Patient Record")
    print("7. Exit Nimbus Health")

    # Get user choice
    choice = input("Choose an option: ")

    # Exit the program
    if choice == "7":
        break

    # Choice 1: Show active patients
    if choice == "1":
        patient_list = patient_repo.get_patients("active")
        counts = patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "active")
        

    elif choice == "2":
    #Choice 2: Show inactive patients
        patient_list = patient_repo.get_patients("inactive")
        counts = patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "inactive")

    
    elif choice == "3":
    #Choice 3: Show all patients
        patient_list = patient_repo.get_patients("all")
        counts = patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "all")


    elif choice == "4":
    #Choice 4: Register a new patient
        # Validate that the name contains only letters and spaces
        while True:
            name = input("Enter patient name: ")
            if name.replace(" ", "").isalpha():
                break
            else:
                print("Please enter a valid name.")
        # Validate that the age is a number
        while True:
            try:
                age = int(input("Enter patient age: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        # Validate that the doctor name contains only letters and spaces
        while True:
            doctor = input("Enter Doctor’s  name: ")
            if doctor.replace(" ", "").isalpha():
                break
            else:
                print("Please enter a valid doctor name.")
        patients.register_patient(name, age, doctor)


    elif choice == "5":
    # Choice 5: Search for a patient by ID
    # Validate that the patient ID is a number
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))
            except ValueError:
                print("Please enter a valid patient ID.")
                continue

            patient = patients.find_patient(patient_id)

            # Validate that the patient exists
            if patient is None:
                print("Patient not found.")
                continue

            break

        print("Patient Found:")
        print("-------------")

        # Show patient details
        patients.show_patient_details(patient)
        print(f"Active: {patient['active']}")

    elif choice == "6":
        # Choice 6: Update a patient record

        # Validate that the patient ID is a number
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))
            except ValueError:
                print("Please enter a valid patient ID.")
                continue

            patient = patients.find_patient(patient_id)

            if patient is None:
                print("Patient not found.")
                continue
            break

        # Keep updating this patient
        while True:
            print("What would you like to update?")
            print("1. Name")
            print("2. Age")
            print("3. Doctor")
            print("4. Patient Status")
            print("5. Done")

            update_choice = input("Choose an option: ")

            if update_choice == "1":
                while True:
                    updated_name = input("Enter new name: ")

                    if updated_name.replace(" ", "").isalpha():
                        break
                    else:
                        print("Please enter a valid name.")

                patients.update_patient(patient_id, name=updated_name)

            elif update_choice == "2":
                while True:
                    try:
                        updated_age = int(input("Enter new age: "))
                        break
                    except ValueError:
                        print("Please enter a valid number.")

                patients.update_patient(patient_id, age=updated_age)

            elif update_choice == "3":
                while True:
                    updated_doctor = input("Enter new doctor: ")

                    if updated_doctor.replace(" ", "").isalpha():
                        break
                    else:
                        print("Please enter a valid doctor name.")

                patients.update_patient(patient_id, doctor=updated_doctor)

            elif update_choice == "4":
                if patient["active"]:
                    print("Current status: Active")
                else:
                    print("Current status: Inactive")

                print("1. Activate Patient")
                print("2. Deactivate Patient")
                print("3. Cancel")

                status_choice = input("Choose an option: ")

                if status_choice == "1":
                    if patient["active"]:
                        print("Patient is already active.")
                    else:
                        patient["active"] = True
                        patients.patient_repo.save_patients(patients.patients)
                        print(f"Patient {patient_id} reactivated successfully!")

                elif status_choice == "2":
                    if not patient["active"]:
                        print("Patient is already inactive.")
                    else:
                        patient["active"] = False
                        patients.patient_repo.save_patients(patients.patients)
                        print(f"Patient {patient_id} deactivated successfully!")

                elif status_choice == "3":
                    print("Status update cancelled.")

                else:
                    print("Invalid option. Please choose a valid menu option.")

            elif update_choice == "5":
                print("Update complete.")
                break

            else:
                print("Invalid option. Please choose a valid menu option.")
