import os
import boto3
from dotenv import load_dotenv
import subprocess

# Load environment variables from the .env file
load_dotenv()

# Constants
ROOT_DIR = "."
LOG_DIR_RT = "ManyDaughters_RT_AnalysisPackage/log"  # Local directory to store log files for RT
PROCESSED_LOG_DIR_RT = os.path.join(LOG_DIR_RT, 'processed')
LOG_DIR_PC = "ManyDaughters_PC_AnalysisPackage_95/log"  # Local directory to store log files for PC
CENSORED_LOG_DIR_PC = os.path.join(LOG_DIR_PC, 'censored')
RESULTS_DIR = "ManyDaughters_RT_AnalysisPackage/out/checked"  # Local directory of stored results from computational reproducibility check
SUMMARY_DIR = "summary"  # Local directory to store summary JSON files

UPLOADED_LOG_DIR_RT = os.path.join(LOG_DIR_RT, 'uploaded')
UPLOADED_LOG_DIR_PC = os.path.join(LOG_DIR_PC, 'uploaded')
UPLOADED_RESULTS_DIR = "ManyDaughters_RT_AnalysisPackage/out/uploaded"
UPLOADED_SUMMARY_DIR = os.path.join(SUMMARY_DIR, 'uploaded')

# Create the uploaded files directories if they don't exist
if not os.path.exists(UPLOADED_LOG_DIR_RT):
    os.makedirs(UPLOADED_LOG_DIR_RT)
if not os.path.exists(UPLOADED_LOG_DIR_PC):
    os.makedirs(UPLOADED_LOG_DIR_PC)
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
    except Exception as e:
        print(f"Error uploading file: {e}")

def move_file_to_uploaded(file_path, uploaded_dir):
    file_name = os.path.basename(file_path)
    new_path = os.path.join(uploaded_dir, file_name)
    os.rename(file_path, new_path)
    print(f"Moved {file_name} to {uploaded_dir}")

def upload_files():
    # Upload log files from RT
    for filename in os.listdir(PROCESSED_LOG_DIR_RT):
        if filename.endswith('.log'):
            file_path = os.path.join(PROCESSED_LOG_DIR_RT, filename)
            s3_key = f'stata/logs/{filename}'
            upload_to_s3(file_path, s3_key)
            move_file_to_uploaded(file_path, UPLOADED_LOG_DIR_RT)
    
    # Upload log files from PC
    for filename in os.listdir(CENSORED_LOG_DIR_PC):
        if filename.endswith('.log'):
            file_path = os.path.join(CENSORED_LOG_DIR_PC, filename)
            s3_key = f'stata/logs/{filename}'
            upload_to_s3(file_path, s3_key)
            move_file_to_uploaded(file_path, UPLOADED_LOG_DIR_PC)
    
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
            
            # Extract identifier for curl command
            identifier = filename.replace('.json', '')
            
            # Execute curl command for real-time updates
            curl_command = f'curl "https://www.manydaughters.com/api/stata?stataJob={identifier}"'
            subprocess.run(curl_command, shell=True)
            print(f"Executed curl command: {curl_command}")

if __name__ == "__main__":
    upload_files()

