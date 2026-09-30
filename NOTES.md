# Nimbus Health Dev Notes 🏥

Personal cheat sheet for building and maintaining Nimbus Health.

---

# Running Nimbus

Start the program:

```bash
python3 main.py
```

---

# Python Reminders 🐍

## Run a Python file

```bash
python3 filename.py
```

Example:

```bash
python3 main.py
```

---

## Importing modules

Example:

```python
import json
```

This gives access to JSON tools.

---

# JSON Reminders 💾

## JSON vs Python syntax

JSON:

```json
{
  "active": true
}
```

Python:

```python
{
    "active": True
}
```

Remember:

- JSON uses `true` / `false`
- Python uses `True` / `False`

---

## JSON requires double quotes

Correct:

```json
{
  "name": "Jane Doe"
}
```

Incorrect:

```json
{
  "name": "Jane Doe"
}
```

---

## Loading JSON into Python

```python
import json

def load_patients():
    with open("patients.json", "r") as file:
        return json.load(file)
```

Flow:

```
patients.json
      ↓
json.load()
      ↓
Python list/dictionary
      ↓
patients variable
```

---

## Saving Python data to JSON

```python
def save_patients():
    with open("patients.json", "w") as file:
        json.dump(patients, file, indent=4)
```

Flow:

```
Python data
      ↓
json.dump()
      ↓
patients.json
```

---

# Git Commands 🌱

## Check current status

```bash
git status
```

Shows:

- current branch
- changed files
- staged files
- commit status

---

## View commits

Short version:

```bash
git log --oneline
```

Detailed version:

```bash
git log
```

---

## View branches

```bash
git branch
```

The `*` shows your current branch.

Example:

```
* feature/json-storage
  main
```

---

## Create a branch

```bash
git branch branch-name
```

Example:

```bash
git branch feature/json-storage
```

---

## Switch branches

```bash
git switch branch-name
```

Example:

```bash
git switch main
```

---

## Stage changes

Stage everything:

```bash
git add .
```

Stage one file:

```bash
git add filename
```

Example:

```bash
git add patients.json
```

---

## Commit changes

```bash
git commit -m "message"
```

Examples:

```bash
git commit -m "Add JSON patient loading"
```

Good commit messages:

- Add feature
- Fix bug
- Update documentation
- Refactor code

---

## Push to GitHub

First time:

```bash
git push -u origin main
```

After that:

```bash
git push
```

---

## Check differences

See what changed:

```bash
git diff
```

Specific file:

```bash
git diff filename
```

Example:

```bash
git diff patients.py
```

---

# Git Workflow 🔄

The normal cycle:

```
Change code
    ↓
git status
    ↓
git add .
    ↓
git commit -m "message"
    ↓
git push
```

---

# Current Nimbus Branch 🌿

Current feature:

```
feature/json-storage
```

Goal:

Add:

- JSON loading ✅
- JSON saving
- Persistent patient records

---

# Common Reminders 🧠

Before committing:

✅ Test the program  
✅ Check git status  
✅ Make sure changes are intentional

Before debugging:

1. Read the error
2. Check the file/line
3. Verify assumptions
4. Test a small change

# Future Feature Ideas

## Patient Status Visibility / History

**Discovery:**
During smoke testing, discovered a workflow issue with deactivated patients.

**Problem:**
Previously, the application only displayed active patients. If a patient was deactivated:

- They disappeared from normal patient views
- Reactivating required knowing the patient ID
- Users had no easy way to locate inactive records

**Implemented:**

- Added ability to view active patients
- Added ability to view inactive/deactivated patients
- Added ability to view all patient records
- Added repository method `get_patients(status)` to support flexible status-based retrieval
- Added repository method `get_patient_counts()` for overall patient statistics
- Updated patient display logic to show status-appropriate counts
- Retired the old `load_patients()` repository method
- Updated the main menu to expose Active, Inactive, and All patient views

**Current UX:**

- Active patients remain the default/common workflow
- Inactive patients can be accessed when needed
- All patients can be viewed when a complete record list is needed
- View Active displays total records + active count
- View Inactive displays total records + inactive count
- View All displays total records only

**Future Consideration:**

- Display explicit Active/Inactive status on individual patient records when using View All
- Consider adding patient activity history/audit tracking
- Consider historical record tracking for future enterprise features

## Patient ID Input UX

**Discovery:**
During smoke testing, discovered two patient ID workflow issues.

**Problem 1 — Invalid ID format:**

- Entering a non-numeric patient ID could raise an unhandled `ValueError`
- Example: entering `j` caused the application to crash instead of providing a user-friendly error

**Implemented:**

- Added `ValueError` handling for patient ID input
- Invalid/non-numeric IDs now display a user-friendly error message
- Users can retry without crashing or leaving the current workflow

**Problem 2 — Patient not found:**

- A valid but nonexistent patient ID previously displayed "Patient not found" and returned the user to the main menu
- This could be frustrating if the user simply mistyped the ID

**Implemented:**

- Search now allows the user to retry when a patient is not found
- Update now allows the user to retry when a patient is not found
- Users remain within the current Search/Update workflow instead of being returned to the main menu

## Patient Update Workflow UX

**Discovery:**
During smoke testing, discovered that updating a patient record returned the user to the main menu after each individual change.

**Previous workflow:**

- User selects Update Patient Record
- Enters the patient ID
- Makes one change
- Application returns to the main menu

**Implemented:**

- Update workflow now remains open after a successful change
- Users can update multiple fields during the same session
- Added a "Done" option to finish updating the patient
- Selected patient remains in context, so the user does not need to re-enter the patient ID for each change
- Invalid or nonexistent patient IDs can be retried without restarting the operation
- Status updates now use the same `patients.update_patient()` pathway as name, age, and doctor updates
- `update_patient()` now supports updating the `active` field
- Repository update operations now return whether a patient record was actually updated
- Removed duplicate success messaging so users receive one clear confirmation for each update

**Current workflow:**
Update Patient Record
↓
Enter Patient ID
↓
Find Patient
↓
Update Menu
↓
Make Change
↓
Return to Update Menu
↓
Make Another Change OR Done
↓
Return to Main Menu
