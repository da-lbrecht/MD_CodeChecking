import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(["python", script_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        run_script(script)

if __name__ == "__main__":
    main()
