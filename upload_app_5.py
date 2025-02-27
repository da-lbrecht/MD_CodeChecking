import os
import boto3
from dotenv import load_dotenv
import subprocess

# Load environment variables from the .env file
load_dotenv()

# Constants
ROOT_DIR = "."
LOG_DIR = "ManyDaughters_RT_AnalysisPackage/log"  # Local directory to store log files
PROCESSED_LOG_DIR = os.path.join(LOG_DIR, 'processed')
RESULTS_DIR = "ManyDaughters_RT_AnalysisPackage/out/checked"  # Local directory of stored results from computational reproducibility check
SUMMARY_DIR = "ManyDaughters_RT_AnalysisPackage/summary"  # Local directory to store summary JSON files

UPLOADED_LOG_DIR = os.path.join(LOG_DIR, 'uploaded')
UPLOADED_RESULTS_DIR = "ManyDaughters_RT_AnalysisPackage/out/uploaded"
UPLOADED_SUMMARY_DIR = os.path.join(SUMMARY_DIR, 'uploaded')

# Create the uploaded files directories if they don't exist
if not os.path.exists(UPLOADED_LOG_DIR):
    os.makedirs(UPLOADED_LOG_DIR)
if not os.path.exists(UPLOADED_SUMMARY_DIR):
    os.makedirs(UPLOADED_SUMMARY_DIR)

def upload_to_s3(file_path, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('S3_Access_Key_ID'),
        aws_secret_access_key=os.getenv('S3_Secret_Access_Key'),
        region_name='us-east-1'
    )
    bucket_name = 'many-daughters'
    
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
        
        # Extract identifier for curl command
        file_name = os.path.basename(file_path)
        if file_name.endswith('_5%.log'):
            identifier = file_name.replace('_5%.log', '')
        elif file_name.endswith('_95%.log'):
            identifier = file_name.replace('_95%.log', '')
        elif file_name.endswith('_results.csv'):
            identifier = file_name.replace('repro_', '').replace('_results.csv', '')
        elif file_name.endswith('.json'):
            identifier = file_name.replace('.json', '')
        else:
            identifier = None
        
        # Execute curl command for real-time updates
        if identifier:
            curl_command = f'curl "https://www.manydaughters.com/api/stata?stataJob={identifier}"'
            subprocess.run(curl_command, shell=True)
            print(f"Executed curl command: {curl_command}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def move_file_to_uploaded(file_path, uploaded_dir):
    file_name = os.path.basename(file_path)
    new_path = os.path.join(uploaded_dir, file_name)
    os.rename(file_path, new_path)
    print(f"Moved {file_name} to {uploaded_dir}")

def upload_files():
    # Upload log files
    for filename in os.listdir(PROCESSED_LOG_DIR):
        if filename.endswith('.log'):
            file_path = os.path.join(PROCESSED_LOG_DIR, filename)
            s3_key = f'stata/logs/{filename}'
            upload_to_s3(file_path, s3_key)
            move_file_to_uploaded(file_path, UPLOADED_LOG_DIR)
    
    # Upload result files
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith('.csv'):
            file_path = os.path.join(RESULTS_DIR, filename)
            s3_key = f'stata/results/{filename}'
            upload_to_s3(file_path, s3_key)
            move_file_to_uploaded(file_path, UPLOADED_RESULTS_DIR)
    
    # Upload summary JSON files
    for filename in os.listdir(SUMMARY_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(SUMMARY_DIR, filename)
            s3_key = f'stata/summary/{filename}'
            upload_to_s3(file_path, s3_key)
            move_file_to_uploaded(file_path, UPLOADED_SUMMARY_DIR)

if __name__ == "__main__":
    upload_files()

