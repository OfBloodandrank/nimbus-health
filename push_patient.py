import boto3
from botocore.exceptions import ClientError

def push_single_patient():
    print("📡 Packaging patient data packet...")
    
    # Initialize connection to your personal AWS account
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('NimbusHealthRecords')
    
    # Create a realistic test profile item matching your NoSQL schema design
    test_patient = {
        "patient_id": "PATIENT#00001",
        "record_type": "PROFILE",
        "name": "Alice Smith",
        "age": 31,
        "doctor": "Dr. Davis",
        "active": True
    }
    
    try:
        print("🚀 Transmitting record payload to AWS data center...")
        table.put_item(Item=test_patient)
        print("✅ Success! Patient record successfully stored inside NimbusHealthRecords in the cloud.")
        
    except ClientError as e:
        print(f"❌ Transmission failed: {e}")

if __name__ == "__main__":
    push_single_patient()
