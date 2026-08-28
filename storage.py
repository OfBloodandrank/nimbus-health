import sqlite3

def get_connection(db_path="nimbus.db"):
    return sqlite3.connect(db_path)


def initialize_database(db_path="nimbus.db"):
    connection = get_connection(db_path)
    """Create database tables if they do not exist."""

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            doctor TEXT,
            active INTEGER
        )
    """)
    connection.commit()
    connection.close()

initialize_database()

class PatientRepository:
    """Handles patient record database operations."""
    def __init__(self, db_path="nimbus.db"):self.db_path = db_path
    
    def add_patient(self, patient): 

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
        
        patient["id"] = cursor.lastrowid
        
        connection.commit()
        connection.close()



    def save_patients(self, patients):
        """Save patient records to the SQLite database."""

        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        for patient in patients:
            if "id" in patient:
                cursor.execute(
                    "SELECT id FROM patients WHERE id = ?",
                    (patient["id"],)
                )
                existing_patient = cursor.fetchone()

                if existing_patient:
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
        connection.commit()
        connection.close()


    def update_patient(self, patient): 
        """Update an existing patient record in the SQLite database."""

        connection = get_connection(self.db_path)
        cursor = connection.cursor()
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

    def get_patients(self, status):
        """Retrieve patients based on status."""

        connection = get_connection(self.db_path)
        cursor = connection.cursor()

        if status == "active":
            cursor.execute(
                "SELECT * FROM patients WHERE active = ?",
                (1,)
            )

        elif status == "inactive":
            cursor.execute(
                "SELECT * FROM patients WHERE active = ?",
                (0,)
            )

        elif status == "all":
            cursor.execute(
                "SELECT * FROM patients"
            )

        else:
            raise ValueError("Invalid patient status")

        rows = cursor.fetchall()
        

        patients = []

        for row in rows:
            patients.append({
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "doctor": row[3],
        "active": bool(row[4])
    })

        connection.close()

        return patients

    def get_patient_counts(self):
        """Retrieve patient counts by status."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(active) AS active,
                COUNT(*) - SUM(active) AS inactive
            FROM patients
        """)
        counts = cursor.fetchone()
        
        return {
        "total": counts[0],
        "active": counts[1],
        "inactive": counts[2]
    }

    connection = get_connection()
    cursor = connection.cursor()     