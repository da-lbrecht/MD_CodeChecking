import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
GITHUB_REPO = "ManyDaughters/RT_uploads"
DIRECTORY_PATH = "log-files"
ROOT_DIR = "."
LOG_DIR = "ManyDaughters_RT_AnalysisPackage/log"  # Local directory to store log files
MD_PAT = os.getenv('GITHUB_ManyDaughters_PAT')  # Make sure this line correctly retrieves the token

CENSORED_DIR = os.path.join(LOG_DIR, 'censored')
UPLOADED_DIR = os.path.join(LOG_DIR, 'uploaded')

# Create the uploaded files directory if it doesn't exist
if not os.path.exists(UPLOADED_DIR):
    os.makedirs(UPLOADED_DIR)

def upload_file_to_github(file_path, repo, directory):
    file_name = os.path.basename(file_path)
    url = f"https://api.github.com/repos/{repo}/contents/{directory}/{file_name}"
    headers = {
        'Authorization': f'token {MD_PAT}',
        'Content-Type': 'application/json'
    }
    
    with open(file_path, 'rb') as f:
        content = f.read()
    
    data = {
        "message": f"Upload {file_name}",
        "content": base64.b64encode(content).decode('utf-8')  # Encode file content to base64
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Uploaded {file_name} successfully.")
        return True
    else:
        print(f"Failed to upload {file_name}. Status code: {response.status_code}, Response: {response.json()}")
        return False

def move_file_to_uploaded(file_path):
    file_name = os.path.basename(file_path)
    new_path = os.path.join(UPLOADED_DIR, file_name)
    os.rename(file_path, new_path)
    print(f"Moved {file_name} to {UPLOADED_DIR}")

def upload_files():
    for filename in os.listdir(CENSORED_DIR):
        if filename.endswith('.log'):
            file_path = os.path.join(CENSORED_DIR, filename)
            if upload_file_to_github(file_path, GITHUB_REPO, DIRECTORY_PATH):
                move_file_to_uploaded(file_path)

if __name__ == "__main__":
    upload_files()

