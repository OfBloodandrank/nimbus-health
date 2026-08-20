import patients

# Main program loop
while True:
    print("🏥 NIMBUS HEALTH")
    print("1. View Active Patients")
    print("2. Register Patient")
    print("3. Search for a Patient")
    print("4. Update Patient Record")
    print("5. Exit Nimbus Health")

    # Get user choice
    choice = input("Choose an option: ")

    # Exit the program
    if choice == "5":
        break

    #choice 1: Show all patients
    if choice == "1":
        patients.show_patients()


    #choice 2: Register a new patient
    elif choice == "2":
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


    #choice 3: Search for a patient by ID
    elif choice == "3":
        # Validate that the patient ID is a number
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))
                break
            except ValueError:
                print("Please enter a valid patient ID.")
        patient = patients.find_patient(patient_id)
        # Validate that the patient exists
        if patient is None:
            print("Patient not found.")
        else:
           print("Patient Found:")
           print("-------------")
           # Show patient details
           patients.show_patient_details(patient)
           print(f"Active: {patient['active']}")


    #choice 4: Update a patient record
    elif choice == "4":
        # Validate that the patient ID is a number
        patient_id = int(input("Enter patient ID: "))
        patient = patients.find_patient(patient_id)
        if patient is None:
            print("Patient not found.")
        else:
            print("What would you like to update?")
            print("1. Name")
            print("2. Age")
            print("3. Doctor")
            print("4. Patient Status")
            print("5. Cancel")

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
                # Validate that the patient status is either active or inactive
                if patient["active"]:
                    print("Current status: Active")
                else:
                    print("Current status: Inactive")

                print("1. Activate Patient")
                print("2. Deactivate Patient")
                print("3. Cancel")

                # Validate the status choice
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


            #choice 5: Cancel the update
            elif update_choice == "5":
                print("Update cancelled.")
    #if the user enters an invalid option, display an error message
    else:
        print("Invalid option. Please choose a valid menu option.")   
