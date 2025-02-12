import boto3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
S3_BUCKET = "many-daughters"
S3_DIRECTORY_PATH = "stata/codes"
DOWNLOAD_DIR = "ManyDaughters_PC_AnalysisPackage_95/code"  # Local directory to store downloaded files
S3_ACCESS_KEY_ID = os.getenv('S3_Access_Key_ID')  # Correctly retrieve the access key ID
S3_SECRET_ACCESS_KEY = os.getenv('S3_Secret_Access_Key')  # Correctly retrieve the secret access key

# Create a local download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

EXECUTED_DIR = os.path.join(DOWNLOAD_DIR, "checked")  # Subfolder for executed files

# Create the executed files directory if it doesn't exist
if not os.path.exists(EXECUTED_DIR):
    os.makedirs(EXECUTED_DIR)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

# Function to list files in the specified S3 directory
def list_s3_files(bucket, directory):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=directory)
        if 'Contents' in response:
            return [item['Key'] for item in response['Contents']]
        else:
            return []
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

# Function to download a file from S3
def download_file_from_s3(bucket, key, download_path):
    try:
        s3_client.download_file(bucket, key, download_path)
    except s3_client.exceptions.NoSuchKey:
        print(f"The specified key does not exist: {key}")
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '403':
            print(f"Access denied for key: {key}")
        else:
            print(f"An error occurred while downloading {key}: {e}")
    except Exception as e:
        print(f"An error occurred while downloading {key}: {e}")

def download_files():
    try:
        files = list_s3_files(S3_BUCKET, S3_DIRECTORY_PATH)
        
        for file_key in files:
            file_name = os.path.basename(file_key)
            
            # Check if the file already exists in the local directory or executed directory
            local_file_path = os.path.join(DOWNLOAD_DIR, file_name)
            executed_file_path = os.path.join(EXECUTED_DIR, file_name)
            if not os.path.exists(local_file_path) and not os.path.exists(executed_file_path):
                print(f"Downloading {file_name} from S3...")
                download_file_from_s3(S3_BUCKET, file_key, local_file_path)
            else:
                print(f"{file_name} already exists. Skipping download.")

        print("Download complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_files()
