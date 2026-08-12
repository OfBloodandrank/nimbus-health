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
    'name': 'Jane Doe'
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

---

# Nimbus History

## Version 1.0

Completed:
- Patient registration
- Patient search
- Patient updates
- Patient status changes
- Input validation
- README
- GitHub setup

## Version 1.1 - JSON Storage

Completed:
- Created feature branch
- Created patients.json
- Moved patient records to JSON
- Added JSON loading

Next:
- Add save functionality
- Test persistence