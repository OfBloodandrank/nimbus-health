# Nimbus Health 🏥

A Python-based healthcare data management project focused on patient records, validation, auditing, and cloud-ready architecture.

## Overview

Nimbus Health models how healthcare applications can manage sensitive patient information while preserving data integrity, traceability, and operational reliability. The project combines a modular Python workflow with a cloud-native DynamoDB persistence layer built using `boto3`.

It supports:

- patient registration and lifecycle management
- validation of critical patient fields
- profile updates and record status changes
- compliance-focused activity tracking
- migration toward managed cloud infrastructure

---

## Skills Demonstrated

- Python application design and modular architecture
- Healthcare data modeling and patient record handling
- Validation and data integrity logic
- Audit trail and compliance-oriented record tracking
- AWS DynamoDB design and single-table modeling
- `boto3` integration for cloud persistence
- Automated testing with `pytest` and Moto

---

## Impact and Outcomes

This project shows how to design and evolve a healthcare application from a simple local workflow into a cloud-aware data architecture. It emphasizes reliability through validation, traceability through activity history, and scalability through a NoSQL single-table design.

The result is a system that better reflects real-world healthcare software requirements: clean patient operations, dependable records, and a foundation for future cloud deployment and operational growth.

---

## Project Goals

- Provide a clean patient management workflow for healthcare-style records
- Enforce strong validation rules before data is stored
- Preserve an activity trail for compliance and auditing
- Move the persistence layer from local patterns toward cloud-native infrastructure
- Keep the code modular, testable, and easy to extend

---

## Why This Project Matters

Nimbus Health demonstrates how to build healthcare-facing software with strong data integrity, auditability, and cloud migration thinking. It focuses on the operational realities that matter in production systems: reliable validation, clean patient workflows, traceable history, and a database design that scales beyond a local setup.

For recruiters and technical reviewers, this project reflects hands-on learning in Python, AWS service integration, data modeling, and disciplined engineering practices in a domain where correctness and accountability are critical.

---

## Architecture

The application is split into clear responsibilities:

- [main.py](main.py): command-line application entry point
- [patients.py](patients.py): business logic, record validation, and patient operations
- [storage.py](storage.py): DynamoDB repository layer for persistence and querying

This keeps the business rules separate from the data layer, which makes it easier to evolve the project as it moves toward AWS deployment.

---

## Core Features

- Patient registration with sequential numeric IDs
- Update support for name, age, doctor, and active/inactive status
- Audit trail generation for each meaningful patient change
- Input validation for names, ages, doctors, and status values
- Single-table DynamoDB design for profile and activity records
- Automated testing with `pytest` and Moto-based AWS mocking

---

## Technology Stack

- Python 3.x
- AWS DynamoDB
- `boto3`
- `pytest`
- `moto`

---

## Repository Structure

```text
nimbus-health/
├── main.py                  # CLI entry point
├── patients.py              # Business logic and validation
├── storage.py               # DynamoDB repository layer
├── tests/
│   ├── test_cloud_storage.py
│   └── test_patients.py
├── requirements.txt         # Python dependencies
├── README.md                # Project overview and setup
├── NOTES.md                 # Development notes
├── create_table.py          # Table creation helper
├── cloud_sandbox.py         # AWS connectivity smoke test
├── generate_report.py       # Reporting utility
└── nimbus_compliance_snapshot.txt
```

---

## Local Setup

```bash
# Clone the repository
git clone https://github.com/OfBloodandrank/nimbus-health.git

# Navigate into the project folder
cd nimbus-health

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run tests

```bash
python -m pytest -q
```

The local test suite uses mocked DynamoDB behavior through Moto, so it validates the cloud-style repository without requiring live AWS access.

---

## DynamoDB Design

The repository uses a single DynamoDB table with a compound key:

- `patient_id` as the hash key
- `record_type` as the sort key

This allows profile data and compliance activity to coexist in the same table while still supporting efficient lookups by patient.

### Example profile item

```python
profile_item = {
    "patient_id": "PATIENT#00001",
    "record_type": "PROFILE",
    "name": "Jane Doe",
    "age": 22,
    "doctor": "Dr. Robinavitch",
    "active": True
}
```

### Example activity item

```python
registration_log = {
    "patient_id": "PATIENT#00001",
    "record_type": "LOG#REGISTRATION",
    "action": "Patient registered",
    "old_value": "None",
    "new_value": "Registered under doctor Dr. Robinavitch"
}
```

This pattern supports a clean single-table model for both patient data and event history.

---

## Current Status

This project is currently in the AWS migration phase. The application logic and persistence layer have already moved to a DynamoDB-oriented repository, and the test suite validates that behavior with mocked cloud infrastructure.

### Completed

- patient registration logic
- validation and data integrity checks
- patient update flows
- activity history tracking
- DynamoDB repository implementation
- Moto-powered automated testing

### Current Focus

- aligning infrastructure and documentation with the live cloud model
- validating cloud interactions and repository behavior
- preparing for real AWS environment deployment

---

## Roadmap

- [x] Build core patient management workflow
- [x] Add validation and audit-trail patterns
- [x] Move persistence layer to AWS DynamoDB with `boto3`
- [ ] Provision and validate a real AWS environment
- [ ] Deploy the app to a managed cloud runtime
- [ ] Add CI/CD and infrastructure automation

---

## Notes

This project is no longer built around SQLite as its active persistence layer. The code, tests, and documentation are aligned to the current DynamoDB-based architecture.
