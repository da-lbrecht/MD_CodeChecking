import subprocess
import sys
import os
from dotenv import load_dotenv

def run_script(script_name):
    try:
        # Load environment variables from the .env file
        load_dotenv()

        # Use the Python interpreter from the virtual environment
        python_executable = sys.executable
        result = subprocess.run([python_executable, script_name], check=True, env=os.environ.copy())
        print(f"Executed {script_name} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

def main():
    scripts = [
        "download_app.py",
        "stata_runner_app_5.py",
        "stata_runner_app_95.py",
        "log_process_app_5.py",
        "log_process_app_95.py",
        "checker_app.py",
        "upload_app.py"
    ]

    for script in scripts:
        while True:
            user_input = input(f"Do you want to run {script}? (y/n) or exit the application (x): ").strip().lower()
            if user_input == 'y':
                run_script(script)
                break
            elif user_input == 'n':
                print(f"Skipping {script}.")
                break
            elif user_input == 'x':
                print("Exiting.")
                sys.exit(0)
            else:
                print("Invalid input. Please type 'y' to run the script, 'n' to skip, or 'x' to exit.")

if __name__ == "__main__":
    main()
