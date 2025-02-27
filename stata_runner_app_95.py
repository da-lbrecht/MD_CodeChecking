import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
ROOT_DIR = os.path.abspath(".")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95", "code")  # Local directory to store downloaded files
LOG_DIR = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95", "log")  # Local directory to store log files
CSV_DIR = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95", "out")  # Local directory to store results
STATA_EXECUTABLE = "M:/applications/STATA17/StataMP-64.exe"
ANALYSIS_PACKAGE_DIR = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95")  # Relative path inside ROOT_DIR

EXECUTED_DIR = os.path.join(DOWNLOAD_DIR, "checked")  # Subfolder for executed files

# Create the executed files directory if it doesn't exist
if not os.path.exists(EXECUTED_DIR):
    os.makedirs(EXECUTED_DIR)

# Create the log files directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def move_log_file(file_path):
    log_file_name = os.path.basename(file_path).replace('.do', '.log')
    original_log_file = os.path.join(ANALYSIS_PACKAGE_DIR, log_file_name)  # Ensure correct path
    new_log_file = os.path.join(LOG_DIR, log_file_name)
    if os.path.exists(original_log_file):
        os.rename(original_log_file, new_log_file)
        print(f"Moved log file to {new_log_file}")
    else:
        print(f"Log file {original_log_file} not found.")

def rename_csv_file(do_file_name):
    if not os.path.exists(CSV_DIR):
        print(f"CSV directory {CSV_DIR} not found.")
        return
    for file_name in os.listdir(CSV_DIR):
        if file_name.startswith("h") and "_results.csv" in file_name:
            new_file_name = f"repro_{do_file_name}_{file_name}"
            os.rename(os.path.join(CSV_DIR, file_name), os.path.join(CSV_DIR, new_file_name))
            print(f"Renamed {file_name} to {new_file_name}")

def execute_stata_do_file(file_path):
    original_dir = os.getcwd()
    try:
        os.chdir(ANALYSIS_PACKAGE_DIR)
        if not os.path.exists(STATA_EXECUTABLE):
            raise FileNotFoundError(f"Stata executable not found at {STATA_EXECUTABLE}. Please ensure the path is correct.")
        do_file_name = os.path.basename(file_path)[:-6]  # Remove last 6 characters from the do-file name
        result = subprocess.run([STATA_EXECUTABLE, "-e", "do", os.path.relpath(file_path, ANALYSIS_PACKAGE_DIR)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Executed {file_path} successfully.")
        rename_csv_file(do_file_name)
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
    execute_files()
