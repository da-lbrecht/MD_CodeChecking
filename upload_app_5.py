import os
import base64
import requests
import boto3
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
ROOT_DIR = "."
LOG_DIR = "ManyDaughters_RT_AnalysisPackage/log"  # Local directory to store log files
RESULTS_DIR = "ManyDaughters_RT_AnalysisPackage/out/checked" # Local directory of stored results from computational reproducibility check

CENSORED_DIR = os.path.join(LOG_DIR, 'censored')
UPLOADED_DIR = os.path.join(LOG_DIR, 'uploaded')

# Create the uploaded files directory if it doesn't exist
if not os.path.exists(UPLOADED_DIR):
    os.makedirs(UPLOADED_DIR)

def upload_to_s3(file_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('S3_Access_Key_ID'),
        aws_secret_access_key=os.getenv('S3_Secret_Access_Key'),
        region_name='us-east-1'
    )
    bucket_name = 'many-daughters'
    s3_key = f'stata/results/{os.path.basename(file_path)}'
    
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def move_file_to_uploaded(file_path):
    file_name = os.path.basename(file_path)
    new_path = os.path.join(UPLOADED_DIR, file_name)
    os.rename(file_path, new_path)
    print(f"Moved {file_name} to {UPLOADED_DIR}")

def upload_files():
    for filename in os.listdir(CENSORED_DIR):
        if filename.endswith('.log'):
            file_path = os.path.join(CENSORED_DIR, filename)
            upload_to_s3(file_path)
            move_file_to_uploaded(file_path)

if __name__ == "__main__":
    upload_files()

