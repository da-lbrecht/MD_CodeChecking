import boto3
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
S3_BUCKET = "many-daughters"
S3_DIRECTORY_PATHS = ["stata/codes", "stata/results"]
DOWNLOAD_DIRS = {
    "stata/codes": "ManyDaughters_RT_AnalysisPackage/code",
    "stata/results": "ManyDaughters_RT_AnalysisPackage/results"
}
CHECKED_DIRS = {
    "stata/codes": "ManyDaughters_RT_AnalysisPackage/code/checked",
    "stata/results": "ManyDaughters_RT_AnalysisPackage/results/checked"
}
S3_ACCESS_KEY_ID = os.getenv('S3_Access_Key_ID')  # Correctly retrieve the access key ID
S3_SECRET_ACCESS_KEY = os.getenv('S3_Secret_Access_Key')  # Correctly retrieve the secret access key

# Create local download and checked directories if they don't exist
for directory in DOWNLOAD_DIRS.values():
    if not os.path.exists(directory):
        os.makedirs(directory)
for directory in CHECKED_DIRS.values():
    if not os.path.exists(directory):
        os.makedirs(directory)

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
    do_files_downloaded = 0
    csv_files_downloaded = 0
    
    try:
        for s3_directory_path in S3_DIRECTORY_PATHS:
            files = list_s3_files(S3_BUCKET, s3_directory_path)
            download_dir = DOWNLOAD_DIRS[s3_directory_path]
            checked_dir = CHECKED_DIRS[s3_directory_path]
            
            for file_key in files:
                file_name = os.path.basename(file_key)
                
                # Skip files starting with "repro" in the "stata/results" directory
                if s3_directory_path == "stata/results" and file_name.startswith("repro"):
                    continue
                
                # Check if the file already exists in the local directory or checked directory
                local_file_path = os.path.join(download_dir, file_name)
                checked_file_path = os.path.join(checked_dir, file_name)
                if not os.path.exists(local_file_path) and not os.path.exists(checked_file_path):
                    print(f"Downloading {file_name} from S3...")
                    download_file_from_s3(S3_BUCKET, file_key, local_file_path)
                    if file_name.endswith('.do'):
                        do_files_downloaded += 1
                    elif file_name.endswith('.csv'):
                        csv_files_downloaded += 1
                else:
                    print(f"{file_name} already exists. Skipping download.")

        print(f"Download complete. {do_files_downloaded} do-files and {csv_files_downloaded} csv-files downloaded.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_files()
