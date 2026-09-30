
import patients

while True:
    print("\n=== Nimbus Health Patient Portal ===")
    print("1. View Active Patients")
    print("2. View Inactive Patients")
    print("3. View All Patients")
    print("4. Register Patient")
    print("5. Search for a Patient")
    print("6. Update Patient Record")
    print("7. Exit Nimbus Health")

    choice = input("Choose an option: ")

    if choice == "7":
        print("Exiting Nimbus Health. Goodbye.")
        break

    # --- MENU OPTIONS 1, 2, & 3: VIEW DIRECTORIES ---
    if choice == "1":
        patient_list = patients.patient_repo.get_patients("active")
        counts = patients.patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "active")
        
    elif choice == "2":
        patient_list = patients.patient_repo.get_patients("inactive")
        counts = patients.patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "inactive")
    
    elif choice == "3":
        patient_list = patients.patient_repo.get_patients("all")
        counts = patients.patient_repo.get_patient_counts()
        patients.show_patients(patient_list, counts, "all")

    # --- MENU OPTION 4: REGISTER PATIENT ---
    elif choice == "4":
        while True:
            name = input("Enter patient name: ").strip()
            if name.replace(" ", "").isalpha() and name:
                break
            print("Please enter a valid name (letters and spaces only).")

        while True:
            try:
                age = int(input("Enter patient age: "))
                if age >= 0:
                    break
                print("Age cannot be negative.")
            except ValueError:
                print("Please enter a valid integer for age.")

        while True:
            doctor = input("Enter Doctor's name: ").strip()
            if doctor.replace(" ", "").isalpha() and doctor:
                break
            print("Please enter a valid doctor name (letters and spaces only).")

        patients.register_patient(name, age, doctor)

    # --- MENU OPTION 5: SEARCH PATIENT ---
    elif choice == "5":
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))
                break
            except ValueError:
                print("Please enter a valid numeric patient ID.")

        patient = patients.find_patient(patient_id)

        if patient is None:
            print("Patient not found.")
        else:
            print("\nPatient Found:")
            print("-------------")
            patients.show_patient_details(patient)

    # --- MENU OPTION 6: UPDATE PATIENT RECORD ---
    elif choice == "6":
        while True:
            try:
                patient_id = int(input("Enter patient ID to update: "))
                break
            except ValueError:
                print("Please enter a valid numeric patient ID.")

        patient = patients.find_patient(patient_id)

        if patient is None:
            print("Patient not found.")
            continue

        while True:
            print(f"\nUpdating Record for ID {patient_id} ({patient['name']}):")
            print("1. Name")
            print("2. Age")
            print("3. Doctor")
            print("4. Patient Status")
            print("5. Done")

            update_choice = input("Choose an option: ")

            if update_choice == "1":
                while True:
                    updated_name = input("Enter new name: ").strip()
                    if updated_name.replace(" ", "").isalpha() and updated_name:
                        break
                    print("Please enter a valid name.")
                
                if patients.update_patient(patient_id, name=updated_name):
                    print("Name updated successfully.")
                    patient = patients.find_patient(patient_id)

            elif update_choice == "2":
                while True:
                    try:
                        updated_age = int(input("Enter new age: "))
                        if updated_age >= 0:
                            break
                        print("Age cannot be negative.")
                    except ValueError:
                        print("Please enter a valid number.")

                if patients.update_patient(patient_id, age=updated_age):
                    print("Age updated successfully.")
                    patient = patients.find_patient(patient_id)

            elif update_choice == "3":
                while True:
                    updated_doctor = input("Enter new doctor: ").strip()
                    if updated_doctor.replace(" ", "").isalpha() and updated_doctor:
                        break
                    print("Please enter a valid doctor name.")

                if patients.update_patient(patient_id, doctor=updated_doctor):
                    print("Doctor updated successfully.")
                    patient = patients.find_patient(patient_id)

            elif update_choice == "4":
                print(f"Current status: {'Active' if patient['active'] else 'Inactive'}")
                print("1. Activate Patient")
                print("2. Deactivate Patient")
                print("3. Cancel")

                status_choice = input("Choose an option: ")

                if status_choice == "1":
                    if patient["active"]:
                        print("Patient is already active.")
                    else:
                        patients.update_patient(patient_id, active=True)
                        print(f"Patient {patient_id} reactivated successfully!")
                        patient = patients.find_patient(patient_id)

                elif status_choice == "2":
                    if not patient["active"]:
                        print("Patient is already inactive.")
                    else:
                        # Calls our clean, automated manager function!
                        patients.deactivate_patient(patient_id)
                        patient = patients.find_patient(patient_id)

                elif status_choice == "3":
                    print("Status update cancelled.")
                else:
                    print("Invalid option.")

            elif update_choice == "5":
                print("Update session complete.")
                break
            else:
                print("Invalid option. Please choose a valid menu option.")
