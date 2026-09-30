import boto3
from botocore.exceptions import ClientError

class PatientRepository:
    """The data desk that handles all reading and writing to our AWS cloud table."""
    
    def __init__(self, table_name="NimbusHealthRecords"):
        # Initialize connection to the live or mocked AWS DynamoDB infrastructure service
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table(table_name)
    
    def add_patient(self, patient): 
        """Saves a new patient profile and logs an initial registration note into the cloud single-table layout."""
        # 🔢 1. Scan your cloud table items to count how many patient profiles already exist
        counts = self.get_patient_counts()
        next_id = counts["total"] + 1
        
        # 🛡️ Lock the calculated sequential ID number back into the main patient object dictionary
        patient['id'] = next_id
        formatted_id = f"PATIENT#{next_id}"
        
        # 2. Package and transmit the main Patient Profile Item to AWS
        profile_item = {
            "patient_id": formatted_id,
            "record_type": "PROFILE",
            "name": patient["name"],
            "age": int(patient["age"]),
            "doctor": patient["doctor"],
            "active": bool(patient["active"])
        }
        self.table.put_item(Item=profile_item)

        # 3. Package and log the companion Registration Activity log item in the exact same cloud partition space!
        registration_log = {
            "patient_id": formatted_id,
            "record_type": "LOG#REGISTRATION",
            "action": "Patient registered",
            "old_value": "None",
            "new_value": f"Registered under doctor {patient['doctor']}"
        }
        self.table.put_item(Item=registration_log)
        return next_id


    def get_patient_by_id(self, patient_id):
        """Pulls one specific patient profile directly out of our NoSQL cloud partition room."""
        try:
            response = self.table.get_item(
                Key={
                    'patient_id': f"PATIENT#{patient_id}",
                    'record_type': 'PROFILE'
                }
            )
            item = response.get('Item')
            
            # Translate NoSQL internal layout back into our core application dictionary shape
            if item:
                return {
                    "id": patient_id,
                    "name": item.get("name"),
                    "age": int(item.get("age")),
                    "doctor": item.get("doctor"),
                    "active": bool(item.get("active"))
                }
            return None
        except ClientError:
            return None

    def update_patient(self, patient):
        """Updates a patient's info and logs field modifications as history trace items in the cloud."""
        formatted_id = f"PATIENT#{patient['id']}"
        
        # Fetch their current cloud record first to check what changed
        old_record = self.get_patient_by_id(patient['id'])
        if not old_record:
            return False

        # --- AUDIT TRAIL LOGGING GENERATION ---
        if old_record["name"] != patient["name"]:
            self.table.put_item(Item={
                "patient_id": formatted_id,
                "record_type": "LOG#NAME_CHANGED",
                "action": "Name changed",
                "old_value": old_record["name"],
                "new_value": patient["name"]
            })
            
        if old_record["age"] != patient["age"]:
            self.table.put_item(Item={
                "patient_id": formatted_id,
                "record_type": "LOG#AGE_CHANGED",
                "action": "Age changed",
                "old_value": str(old_record["age"]),
                "new_value": str(patient["age"])
            })

        if old_record["doctor"] != patient["doctor"]:
            self.table.put_item(Item={
                "patient_id": formatted_id,
                "record_type": "LOG#DOCTOR_CHANGED",
                "action": "Assigned doctor changed",
                "old_value": old_record["doctor"],
                "new_value": patient["doctor"]
            })

        if old_record["active"] != patient["active"]:
            self.table.put_item(Item={
                "patient_id": formatted_id,
                "record_type": "LOG#STATUS_CHANGED",
                "action": "Status changed",
                "old_value": "Active" if old_record["active"] else "Inactive",
                "new_value": "Active" if patient["active"] else "Inactive"
            })

        # --- SAVE THE NEW CHANGES ---
        profile_item = {
            "patient_id": formatted_id,
            "record_type": "PROFILE",
            "name": patient["name"],
            "age": int(patient["age"]),
            "doctor": patient["doctor"],
            "active": bool(patient["active"])
        }
        self.table.put_item(Item=profile_item)
        return True

    def get_patients(self, status):
        """Pulls a collection list of patient folders filtering and sorting them by their active toggle state and ID."""
        response = self.table.scan()
        items = response.get('Items', [])
        
        patients_list = []
        for item in items:
            if item.get("record_type") == "PROFILE":
                is_active = bool(item.get("active"))
                
                # Safely extract integer value out of the composite key string split handles
                raw_id = item.get("patient_id").split("#")[1]
                
                patient_data = {
                    "id": int(raw_id),
                    "name": item.get("name"),
                    "age": int(item.get("age")),
                    "doctor": item.get("doctor"),
                    "active": is_active
                }
                
                if status == "all":
                    patients_list.append(patient_data)
                elif status == "active" and is_active:
                    patients_list.append(patient_data)
                elif status == "inactive" and not is_active:
                    patients_list.append(patient_data)
                    
        # 🧼 THE GOLD-STAR SORTING FIX: 
        # Sorts the items numerically by their integer ID values before sending them to the screen!
        return sorted(patients_list, key=lambda x: x["id"])


    def get_patient_activity(self, patient_id):
        """Pulls the entire chronological history timeline logs for a patient in a single fetch."""
        response = self.table.scan()
        items = response.get('Items', [])
        
        activity_logs = []
        formatted_id = f"PATIENT#{patient_id}"
        
        for item in items:
            if item.get("patient_id") == formatted_id and item.get("record_type").startswith("LOG#"):
                activity_logs.append({
                    "action": item.get("action"),
                    "old_value": item.get("old_value"),
                    "new_value": item.get("new_value")
                })
        return activity_logs

    def get_patient_counts(self):
        """Calculates our dashboard summary metrics totals directly from our cloud table items."""
        response = self.table.scan()
        items = response.get('Items', [])
        
        total = 0
        active = 0
        inactive = 0
        
        for item in items:
            if item.get("record_type") == "PROFILE":
                total += 1
                if bool(item.get("active")):
                    active += 1
                else:
                    inactive += 1
                    
        return {"total": total, "active": active, "inactive": inactive}
