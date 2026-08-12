# Nimbus Health 🏥

A Python-based patient management system that allows users to manage patient records through a command-line interface.

---

## 🚀 Architectural Overview
Nimbus Health transitions standard clinical workflow management into software automation. The project demonstrates secure data handling, strict data validation loops, and modular programming patterns, simulating production-ready compliance controls required in the health tech sector.

### Core Capabilities & Features
- **Patient Registration:** Seamlessly register new patients with automatically generated unique patient IDs.
- **Granular Profile Updates:** Modify patient names, ages, assigned doctors, and operational records dynamically.
- **Lifecycle Management:** Activate, deactivate, and view active records instantly without compromising historical tracking.
- **Data Integrity Guardrails:** Strict, real-time input validation ensuring invalid datatypes or blank entries cannot corrupt system fields.
  - Validated fields: Patient Names, Ages, Doctor Names, and Unique IDs.

---

## 🛠️ Technology Stack & Core Skills
- **Language:** Python 3.x
- **Development Environment:** Modular Scripting Architecture
- **Version Control:** Git & GitHub Workflow Management
- **Testing Engine:** Python `unittest` framework for automated quality assurance

---

## 📋 Project Directory Structure
```text
nimbus-health/
│
├── main.py        # Main application controller, loop, and interactive user menu
├── patients.py    # Core business logic, data schemas, and management functions
└── README.md      # Professional system documentation
```

---

## ⚙️ Local Installation & Execution

To run the application locally, clone the repository and execute the main controller file:

```bash
# Clone the repository
git clone https://github.com

# Navigate into the project directory
cd nimbus-health

# Execute the application
python3 main.py
```

---

## 🗺️ Cloud & System Evolution Roadmap
This system is undergoing an active engineering transformation to convert it into a resilient, distributed enterprise cloud platform:
- [x] **Phase 1 (Current):** Modularize application logic, build comprehensive terminal input validation, and implement custom object search routines.
- [ ] **Phase 2:** Implement data persistence to replace temporary runtime variables by integrating a local file storage database (JSON/SQLite).
- [ ] **Phase 3:** Migrate the data persistence layer to a fully managed NoSQL cloud database using **AWS DynamoDB** via the Python `boto3` SDK.
- [ ] **Phase 4:** Containerize the application engine using **Docker** for standardized, isolated cloud deployment.
- [ ] **Phase 5:** Orchestrate infrastructure architecture deployment using **Terraform** combined with automated deployment pipelines via **GitHub Actions**.

