# ManyDaughters Code Checking

## Project Description
This project is designed to automate the process of downloading and executing STATA do-files, in order to check for potential errors during execution and for computational reproducibility of analysis results, and provides feedback by uploading checking results and logfiles to an AWS bucket. It consists of seven main applications: download_app.py, stata_runner_app_5.py, stata_runner_app_95.py, log_process_app_5.py,log_process_app_95.py, checker_app.py, upload_app.py.

## Project Structure
```
.env
.gitignore
download_app.py
stata_runner_app_5.py
log_process_app_5.py
repro_checker_app_5.py
upload_app.py
stata_runner_app_95.py
log_process_app_95.py
upload_app.py
ManyDaughters_RT_AnalysisPackage/
    code/
        checked/
        examples/
    data/
        derived/
        raw/
    log/
        censored/
        lib/
        uploaded/
ManyDaughters_PC_AnalysisPackage_95/
    code/
        checked/
        examples/
    data/
        derived/
        raw/
    log/
        censored/
        lib/
        uploaded/
summary/
requirements.txt
```

## Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- Stata 17 (or compatible version)

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
4. Create a [`.env`](.env ) file in the root directory with the following content:
    ```
    GITHUB_ManyDaughters_PAT=your_github_personal_access_token
    S3_Access_Key_ID=your_aws_access_key_id
    S3_Secret_Access_Key=your_aws_secret_access_key
    ```

## Applications

### Download App (`download_app.py`)

This application downloads `.do` files and results from a specified AWS S3 bucket. The `.do` files are saved in both "ManyDaughters_RT_AnalysisPackage" and "ManyDaughters_PC_AnalysisPackage_95" folders, while the results are saved in the "ManyDaughters_RT_AnalysisPackage" folder.

#### Usage

```sh
python download_app.py
```

### Stata Runner App 5% (`stata_runner_app_5.py`)

This application executes the downloaded `.do` files on the 5%-sample using Stata and moves the generated log files to a local directory.

#### Usage

```sh
python stata_runner_app_5.py
```

### Stata Runner App 95% (`stata_runner_app_95.py`)

This application executes the downloaded `.do` files on the 95% data sample using Stata and moves the generated log files to a local directory.

#### Usage

```sh
python stata_runner_app_95.py
```

### Log Process App 5% (`log_process_app_5.py`)

This application processes the log files generated by the Stata Runner App for the 5% data sample, i.e. identifies errors and creates a summary of errors in the first lines of the log files, and moves the processed log files to a designated directory.

#### Usage

```sh
python log_process_app_5.py
```

### Log Process App 95% (`log_process_app_95.py`)

This application processes the log files generated by the Stata Runner App for the 95% data sample, i.e. identifies errors and creates a summary of errors in the first lines of the log files, censors sensitive information, and moves the processed log files to a designated directory.

#### Usage

```sh
python log_process_app_95.py
```

### Checker App (`checker.py`)

This application compares the results of the executed `.do` files with the original results to check for computational reproducibility with the 5% data sample. Additionally the app checks, whether the `.do` files could be executed without errors on the 5% and 95% data samples.

#### Usage

```sh
python checker_app.py
```

### Upload App (`upload_app.py`)

This application uploads reproduced results, log files , and summary JSON files to a specified AWS S3 bucket. 

#### Usage

```sh
python upload_app.py
```

## Execution Order

1. Download files:
    ```sh
    python download_app.py
    ```

2. Execute Stata Runner App 5%:
    ```sh
    python stata_runner_app_5.py
    ```

3. Execute Stata Runner App 95%:
    ```sh
    python stata_runner_app_95.py
    ```

4. Process log files for 5%:
    ```sh
    python log_process_app_5.py
    ```

5. Process log files for 95%:
    ```sh
    python log_process_app_95.py
    ```

6. Check:
    ```sh
    python checker_app.py
    ```

6. Upload files:
    ```sh
    python upload_app.py
    ```

## License

This project is licensed under the Creative Commons Attribution 4.0 International License. You are free to:

- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, see the [LICENSE] file.
