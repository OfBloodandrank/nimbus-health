import sqlite3

connection = sqlite3.connect("nimbus.db")
cursor = connection.cursor()

def initialize_database():
    """Create database tables if they do not exist."""
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

initialize_database()


def load_patients():
    """Load patient records from the SQLite database."""
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

    return patients


def save_patients(patients):
    """Save patient records to the SQLite database."""
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

        else:
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