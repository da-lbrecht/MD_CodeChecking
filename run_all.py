import subprocess
import os
import sys

def run_script(script_name):
    try:
        # Activate the virtual environment and run the script
        activate_venv = os.path.join(os.path.dirname(sys.executable), 'activate')
        command = f"{activate_venv} && python {script_name}"
        result = subprocess.run(command, shell=True, check=True)
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
            user_input = input(f"Do you want to run {script}? (y/n): ").strip().lower()
            if user_input == 'y':
                run_script(script)
                break
            elif user_input == 'n':
                print(f"Skipping {script}.")
                break
            else:
                print("Invalid input. Please type 'y' to run the script or 'n' to skip.")

if __name__ == "__main__":
    main()
