import requests
import os
from dotenv import load_dotenv
import subprocess
import time  # Import the built-in time module

# Load environment variables from the .env file
load_dotenv()

# Constants
GITHUB_REPO = "ManyDaughters/RT_uploads"
DIRECTORY_PATH = "do-files"
ROOT_DIR = "."
DOWNLOAD_DIR = "ManyDaughters_RT_AnalysisPackage/code"  # Local directory to store downloaded files
LOG_DIR = "ManyDaughters_RT_AnalysisPackage/log"  # Local directory to store log files
MD_PAT = os.getenv('GITHUB_ManyDaughters_PAT')  # Make sure this line correctly retrieves the token
STATA_EXECUTABLE = "M:/applications/STATA17/StataMP-64.exe"
ANALYSIS_PACKAGE_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage")  # Relative path inside ROOT_DIR

# Create a local download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

EXECUTED_DIR = os.path.join(DOWNLOAD_DIR, "checked")  # Subfolder for executed files

# Create the executed files directory if it doesn't exist
if not os.path.exists(EXECUTED_DIR):
    os.makedirs(EXECUTED_DIR)

# Create the log files directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Function to get the contents of the specified directory in the GitHub repo
def get_github_files(repo, directory):
    url = f"https://api.github.com/repos/{repo}/contents/{directory}"
    headers = {
        'Authorization': f'token {MD_PAT}',  # Adding the header for authentication
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []

# Function to download a file from GitHub
def download_file(url, file_name):
    response = requests.get(url)
    with open(os.path.join(DOWNLOAD_DIR, file_name), 'wb') as f:
        f.write(response.content)

def move_log_file(file_path):
    log_file_name = os.path.basename(file_path).replace('.do', '.log')
    original_log_file = os.path.join(ANALYSIS_PACKAGE_DIR, log_file_name)  # Ensure correct path
    new_log_file = os.path.join(LOG_DIR, log_file_name)
    if os.path.exists(original_log_file):
        os.rename(original_log_file, new_log_file)
        print(f"Moved log file to {new_log_file}")
    else:
        print(f"Log file {original_log_file} not found.")

def execute_stata_do_file(file_path):
    original_dir = os.getcwd()
    try:
        os.chdir(ANALYSIS_PACKAGE_DIR)
        if not os.path.exists(STATA_EXECUTABLE):
            raise FileNotFoundError(f"Stata executable not found at {STATA_EXECUTABLE}. Please ensure the path is correct.")
        result = subprocess.run([STATA_EXECUTABLE, "-e", "do", os.path.relpath(file_path, ANALYSIS_PACKAGE_DIR)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Executed {file_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file_path}: {e}")
    finally:
        os.chdir(original_dir)
        move_log_file(file_path)

def move_file_to_executed(file_path):
    file_name = os.path.basename(file_path)
    new_path = os.path.join(EXECUTED_DIR, file_name)
    os.rename(file_path, new_path)
    print(f"Moved {file_name} to {EXECUTED_DIR}")

def download_files():
    try:
        files = get_github_files(GITHUB_REPO, DIRECTORY_PATH)
        
        for file in files:
            file_name = file['name']
            file_download_url = file['download_url']
            
            # Check if the file already exists in the local directory or executed directory
            local_file_path = os.path.join(DOWNLOAD_DIR, file_name)
            executed_file_path = os.path.join(EXECUTED_DIR, file_name)
            if not os.path.exists(local_file_path) and not os.path.exists(executed_file_path):
                print(f"Downloading {file_name}...")
                download_file(file_download_url, file_name)
            else:
                print(f"{file_name} already exists. Skipping download.")

        print("Download complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def execute_files():
    try:
        for file_name in os.listdir(DOWNLOAD_DIR):
            local_file_path = os.path.join(DOWNLOAD_DIR, file_name)
            if file_name.endswith('.do'):
                execute_stata_do_file(local_file_path)
                move_file_to_executed(local_file_path)
                
        print("Execution complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_files()
    execute_files()