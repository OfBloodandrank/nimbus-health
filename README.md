# Nimbus Health 🏥

A Python-based patient management system that allows users to manage patient records through a command-line interface.

---

## 🚀 Architectural Overview

Nimbus Health transitions standard clinical workflow management into software automation. The project explores foundational software practices used in healthcare technology systems, including secure data handling, strict validation workflows, modular programming architecture, and database persistence.

### Core Capabilities & Features

- **Patient Registration:** Seamlessly register new patients with automatically generated unique patient IDs.
- **Granular Profile Updates:** Modify patient names, ages, assigned doctors, and record status dynamically.
- **Lifecycle Management:** Activate, deactivate, and view active records instantly without compromising historical tracking.
- **Patient Activity History:** Automatically records patient registration and successful profile changes with timestamps and old/new values for auditability.
- **Data Integrity Guardrails:** Strict, real-time input validation ensuring invalid datatypes or blank entries cannot corrupt system fields.
  - Validated fields: Patient Names, Ages, Doctor Names, and Unique IDs.
- **SQLite Persistence:** Patient records are stored locally in a SQLite database rather than a JSON file.
- **Automated Patient IDs:** SQLite generates unique patient IDs for newly registered records.
- **Automated Testing:** Patient management and database persistence workflows are covered by pytest.

---

## 🛠️ Technology Stack & Core Skills

- **Language:** Python 3.x
- **Development Environment:** Modular Python Architecture
- **Database:** SQLite
- **Version Control:** Git & GitHub Workflow Management
- **Testing:** `pytest` automated testing framework
- **Current Cloud Direction:** AWS DynamoDB and `boto3`

---

## 📋 Project Directory Structure

nimbus-health/
│
├── main.py # Main application controller and interactive user menu
├── patients.py # Core business logic and patient management functions
├── storage.py # SQLite database persistence layer
├── tests/
│ └── test_patients.py # Automated patient management and persistence tests
├── README.md # Project documentation
└── NOTES.md # Developer notes and command cheat sheet

Local SQLite database files are excluded from version control through `.gitignore`.

---

## ⚙️ Local Installation & Execution

To run the application locally, clone the repository and execute the main controller file:

# Clone the repository

git clone https://github.com/OfBloodandrank/nimbus-health.git

# Navigate into the project directory

cd nimbus-health

# Execute the application

python3 main.py

### Running Tests

Nimbus Health uses `pytest` for automated testing.

Run the full test suite with:

python3 -m pytest

The current test suite covers patient validation, SQLite persistence, patient status changes, patient record updates, and patient activity history.

---

## 🗺️ Cloud & System Evolution Roadmap

Nimbus Health is undergoing an active engineering transformation from a local Python application into a resilient, distributed enterprise cloud platform.

- [x] **Phase 1:** Modularize application logic, build comprehensive terminal input validation, and implement custom object search routines.

- [x] **Phase 2:** Implement local SQLite data persistence, migrate patient storage from JSON, expand automated test coverage, and document core functionality.

- [ ] **Phase 3 (Current):** Migrate the data persistence layer to a fully managed NoSQL cloud database using **AWS DynamoDB** via the Python `boto3` SDK.

- [ ] **Phase 4:** Containerize the application engine using **Docker** for standardized, isolated cloud deployment.

- [ ] **Phase 5:** Orchestrate infrastructure architecture deployment using **Terraform** combined with automated deployment pipelines via **GitHub Actions**.

---

## 📊 Current Development Status

🚧 **Nimbus Health is currently transitioning from local database persistence toward cloud-based data infrastructure.**

### Completed

**Core Application Functionality**

- Patient management workflows
- Patient registration
- Patient record updates
- Patient search
- Patient activation/deactivation
- Input validation
- Modular Python architecture

**Data Persistence**

- SQLite-based patient data loading
- SQLite data persistence
- Automated patient ID generation
- Patient record updates and registration
- Migration from JSON storage to SQLite
- Local database files excluded from version control

**Testing & Quality**

- Automated testing with pytest
- Expanded automated test coverage
- SQLite persistence tests
- Patient activity history testing
- End-to-end application smoke testing

**Development Workflow**

- Git/GitHub workflow
- Feature development and version control
- Documentation for core functions
- Database migration committed and pushed to GitHub

### Current Focus

**Patient Activity History**

Nimbus Health is currently expanding its patient persistence layer with activity history and audit-tracking capabilities before beginning the planned migration to AWS DynamoDB.

---

## 📌 Recent Milestone

**SQLite Persistence Migration — Completed**

Nimbus Health successfully migrated its patient persistence layer from JSON file storage to SQLite.

The migration included:

- SQLite database integration
- Patient record loading
- Patient record updates
- New patient insertion
- Database-generated patient IDs
- Python/SQLite data conversion
- Updated automated tests
- Removal of obsolete JSON storage
- Documentation updates
- Successful end-to-end application testing

All automated tests currently pass.
