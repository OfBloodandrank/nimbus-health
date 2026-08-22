import sqlite3

def get_connection():
    return sqlite3.connect("nimbus.db")


def initialize_database():
    """Create database tables if they do not exist."""

    connection = get_connection()
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


    def load_patients(self):
        """Load patient records from the SQLite database."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM patients")
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

    def add_patient(self, patient): 

        connection = get_connection()
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

        connection = get_connection()
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

        connection = get_connection()
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
        connection.commit()
        connection.close()

        