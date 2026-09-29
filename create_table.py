import boto3
from botocore.exceptions import ClientError

def provision_dynamodb_table():
    """Tells AWS to build our compliant single-table NoSQL layout."""
    print("📡 Contacting the AWS cloud infrastructure engine...")
    
    # Initialize our live authorized connection
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
    try:
        # Send the architecture blueprint to Amazon's data center
        response = dynamodb.create_table(
            TableName='NimbusHealthRecords',
            KeySchema=[
                {
                    'AttributeName': 'patient_id',
                    'KeyType': 'HASH'  # HASH = Partition Key (the unique lookup)
                },
                {
                    'AttributeName': 'record_type',
                    'KeyType': 'RANGE' # RANGE = Sort Key (separates profiles from logs)
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'patient_id',
                    'AttributeType': 'S' # S = String data type
                },
                {
                    'AttributeName': 'record_type',
                    'AttributeType': 'S' # S = String data type
                }
            ],
            # On-Demand billing ensures you only pay for what you use (Free Tier friendly)
            BillingMode='PAY_PER_REQUEST'
        )
        print("✅ Table creation initiated successfully!")
        print("⏳ Status: CREATING (AWS is spinning up your cloud table right now...)")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("💡 Notice: The table 'NimbusHealthRecords' already exists in your account!")
        else:
            print(f"❌ Cloud deployment failed: {e}")

if __name__ == "__main__":
    print("=== Nimbus Health Cloud Infrastructure Forge ===")
    provision_dynamodb_table()
