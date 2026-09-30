import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def setup_mock_dynamodb():
    """
    A pytest fixture that safely intercepts boto3 calls, spins up a 
    mock virtual AWS cloud table in your Mac's memory, and tears it down 
    when the test finishes.
    """
    with mock_aws():
        # Open a pipe to our mock memory-based AWS service
        db_resource = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Build a temporary mock table structure matching our schema design
        table = db_resource.create_table(
            TableName='NimbusHealthRecords',
            KeySchema=[
                {'AttributeName': 'patient_id', 'KeyType': 'HASH'},
                {'AttributeName': 'record_type', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'patient_id', 'AttributeType': 'S'},
                {'AttributeName': 'record_type', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Yield lets pytest run the actual tests while keeping this mock table alive
        yield table


# --- AUTOMATED CLOUD TEST ---
def test_mock_patient_insertion(setup_mock_dynamodb):
    """Verifies that our NoSQL dictionary payloads can be written and read cleanly."""
    table = setup_mock_dynamodb
    
    test_payload = {
        "patient_id": "PATIENT#99999",
        "record_type": "PROFILE",
        "name": "Mock Test Patient",
        "age": 45,
        "doctor": "Dr. Sandbox",
        "active": True
    }
    
    # 1. Test writing data into our virtual cloud table
    table.put_item(Item=test_payload)
    
    # 2. Test pulling that data back out using our composite keys
    response = table.get_item(
        Key={
            'patient_id': 'PATIENT#99999',
            'record_type': 'PROFILE'
        }
    )
    
    # 3. Assertions to confirm data integrity
    fetched_item = response.get('Item')
    assert fetched_item is not None
    assert fetched_item['name'] == "Mock Test Patient"
    assert fetched_item['age'] == 45
    assert fetched_item['active'] is True
