# Nimbus Health 🏥

A Python-based patient management system that allows users to manage patient records through a command-line interface.

## Features

- Register new patients
- Automatically generate unique patient IDs
- View active patients
- Search for patients by ID
- Update patient information:
  - Name
  - Age
  - Doctor
  - Patient status
- Activate and deactivate patient records
- Input validation for:
  - Patient names
  - Ages
  - Doctor names
  - Patient IDs

## Technologies

- Python 3

## How to Run

1. Clone this repository
2. Navigate to the project folder
3. Run:

```bash
python3 main.py
```

## Project Structure

```text
nimbus-health/
│
├── main.py        # Main program loop and user menu
├── patients.py    # Patient data and patient management functions
└── README.md      # Project documentation
```

## Future Improvements

- Add data persistence with a database or file storage
- Add more advanced validation
- Create a graphical user interface
- Add authentication and user roles