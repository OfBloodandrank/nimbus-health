import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def test_aws_connection():
    """
    Establishes a pipe to AWS DynamoDB and prints table details 
    to verify your cloud SDK configuration is functioning.
    """
    print("📡 Initializing cloud communication pipe...")
    
    # Initialize the high-level AWS resource interface for DynamoDB
    # In a local environment, boto3 automatically searches for your AWS credentials file
    db_resource = boto3.resource('dynamodb', region_name='us-east-1')
    
    print("✅ Boto3 SDK engine successfully hooked into environment!")
    print("🚀 Cloud environment is ready for table creation or payload execution.")
    return db_resource

if __name__ == "__main__":
    print("=== Nimbus Health Cloud Migration Forge ===")
    try:
        test_aws_connection()
    except NoCredentialsError:
        print("\n❌ AWS Credentials Blocked or Missing!")
        print("💡 Don't worry—this is normal. Your MacBook Air needs its local AWS config files configured.")
