import sqlite3

def get_connection(db_path="nimbus.db"):
    """Opens a fresh connection to the database file."""
    return sqlite3.connect(db_path)


def initialize_database(db_path="nimbus.db"):
    """Creates the tables if they don't exist yet when the app starts."""
    connection = get_connection(db_path)
    cursor = connection.cursor()

    # The main table that stores our patient folders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            doctor TEXT,
            active INTEGER
        )
    """)

    # The history log table that tracks all changes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            action TEXT,
            timestamp TEXT,
            old_value TEXT,
            new_value TEXT
        )
    """)

    connection.commit()
    connection.close()

# Automatically set up the database tables when this file is opened
initialize_database()


class PatientRepository:
    """The data desk that handles all reading and writing to our database file."""
    
    def __init__(self, db_path="nimbus.db"):
        self.db_path = db_path
    
    def add_patient(self, patient): 
        """Saves a brand new patient and writes a 'Patient registered' note in the history log."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patients (name, age, doctor, active)
            VALUES (?, ?, ?, ?)
        """, (
            patient["name"],
            patient["age"],
            patient["doctor"],
            int(patient["active"])
        ))
        
        generated_id = cursor.lastrowid
        patient["id"] = generated_id

        # Write the initial registration note to our history log
        cursor.execute("""
            INSERT INTO patient_activity
            (patient_id, action, timestamp, old_value, new_value)
            VALUES (?, 'Patient registered', datetime('now'), ?, ?)
        """, (generated_id, None, None))
        
        connection.commit()
        connection.close()
        return generated_id

    def update_patient(self, patient):
        """Updates a patient's info and logs any field changes into the history log."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        # Fetch the old folder first so we can compare it to the new changes
        cursor.execute(
            "SELECT name, age, doctor, active FROM patients WHERE id = ?",
            (patient["id"],)
        )
        old_patient = cursor.fetchone()

        if old_patient is None:
            connection.close()
            return False

        # --- HISTORY LOG CHECKS ---

        # 1. Check if the Name changed (Slot 0)
        if old_patient[0] != patient["name"]:
            cursor.execute("""
                INSERT INTO patient_activity (patient_id, action, timestamp, old_value, new_value)
                VALUES (?, 'Name changed', datetime('now'), ?, ?)
            """, (patient["id"], old_patient[0], patient["name"]))

        # 2. Check if the Age changed (Slot 1)
        if old_patient[1] != patient["age"]:
            cursor.execute("""
                INSERT INTO patient_activity (patient_id, action, timestamp, old_value, new_value)
                VALUES (?, 'Age changed', datetime('now'), ?, ?)
            """, (patient["id"], str(old_patient[1]), str(patient["age"])))

        # 3. Check if the Assigned Doctor changed (Slot 2)
        if old_patient[2] != patient["doctor"]:
            cursor.execute("""
                INSERT INTO patient_activity (patient_id, action, timestamp, old_value, new_value)
                VALUES (?, 'Assigned doctor changed', datetime('now'), ?, ?)
            """, (patient["id"], old_patient[2], patient["doctor"]))

        # 4. Check if their Active/Inactive status flipped (Slot 3)
        if bool(old_patient[3]) != patient["active"]:
            old_status = "Active" if old_patient[3] else "Inactive"
            new_status = "Active" if patient["active"] else "Inactive"
            cursor.execute("""
                INSERT INTO patient_activity (patient_id, action, timestamp, old_value, new_value)
                VALUES (?, 'Status changed', datetime('now'), ?, ?)
            """, (patient["id"], old_status, new_status))

        # --- SAVE THE NEW CHANGES ---
        cursor.execute("""
            UPDATE patients
            SET name = ?, age = ?, doctor = ?, active = ?
            WHERE id = ?
        """, (
            patient["name"],
            patient["age"],
            patient["doctor"],
            int(patient["active"]),
            patient["id"]
        ))

        updated = cursor.rowcount > 0
        connection.commit()
        connection.close()
        return updated

    def get_patient_by_id(self, patient_id):
        """Pulls just ONE specific patient folder out of the filing cabinet using their ID."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        connection.close()
        
        # Unpack each item out of its specific slot in the database row container
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "doctor": row[3],
                "active": bool(row[4])
            }
        return None

    def get_patients(self, status):
        """Pulls a list of patients filtered by active or inactive status."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        if status == "active":
            cursor.execute("SELECT * FROM patients WHERE active = ?", (1,))
        elif status == "inactive":
            cursor.execute("SELECT * FROM patients WHERE active = ?", (0,))
        elif status == "all":
            cursor.execute("SELECT * FROM patients")
        else:
            connection.close()
            raise ValueError("Invalid patient status")

        rows = cursor.fetchall()
        connection.close()

        patients = []
        for row in rows:
            patients.append({
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "doctor": row[3],
                "active": bool(row[4])
            })
        return patients

    def get_patient_activity(self, patient_id):
        """Pulls the chronological history log timeline for a single patient."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, patient_id, action, timestamp, old_value, new_value
            FROM patient_activity
            WHERE patient_id = ?
            ORDER BY id ASC
        """, (patient_id,))

        rows = cursor.fetchall()
        connection.close()

        activity = []
        for row in rows:
            activity.append({
                "id": row[0],
                "patient_id": row[1],
                "action": row[2],
                "timestamp": row[3],
                "old_value": row[4],
                "new_value": row[5]
            })
        return activity

    def get_patient_counts(self):
        """Calculates the dashboard metrics (total, active, inactive numbers)."""
        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END),
                SUM(CASE WHEN active = 0 THEN 1 ELSE 0 END)
            FROM patients
        """)
        counts = cursor.fetchone()
        connection.close()
        
        # Safe-fallbacks to ensure an empty database shows 0 instead of crashing
        total = counts[0] if counts and counts[0] is not None else 0
        active = counts[1] if counts and counts[1] is not None else 0
        inactive = counts[2] if counts and counts[2] is not None else 0
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive
        }
