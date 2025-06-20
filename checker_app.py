import os
import pandas as pd
import json

# Constants
ROOT_DIR = os.path.abspath(".")
CSV_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "out")  # Local directory where results from the reproduction check are stored
CSV_DIR_PC = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95", "out")  # Local directory where results from the 95% sample are stored
ORIG_RESULTS_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "results")  # Local directory where submitted results are stored
LOG_DIR_RT = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "log", "processed")  # Local directory to store processed log files from 5% sample
LOG_DIR_PC = os.path.join(ROOT_DIR, "ManyDaughters_PC_AnalysisPackage_95", "log", "censored")  # Local directory to store censored log files from 95% sample
SUMMARY_DIR = os.path.join(ROOT_DIR, "summary")  # Local directory to store summary JSON files

# Ensure the summary directory exists
if not os.path.exists(SUMMARY_DIR):
    os.makedirs(SUMMARY_DIR)

def round_csv_numbers():
    """
    Round numbers in all CSV files in CSV_DIR.
    Numbers are rounded to 6 digits past the decimal point, but if this results in 6 zeros,
    they are rounded to more digits to ensure at least one non-zero digit after the decimal point.
    The rounded numbers are always reported with 6 digits after the decimal point, avoiding scientific notation.
    """
    for file_name in os.listdir(CSV_DIR):
        if file_name.endswith(".csv"):
            file_path = os.path.join(CSV_DIR, file_name)
            print(f"Processing file: {file_path}")
            try:
                df = pd.read_csv(file_path)
                for column in df.select_dtypes(include=['float']):
                    df[column] = df[column].apply(
                        lambda x: f"{x:.6f}" if round(x, 6) != 0 else f"{x:.15f}".rstrip('0').ljust(8, '0')
                    )
                df.to_csv(file_path, index=False)
                print(f"Rounded numbers in {file_name} and saved.")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

def compare_csv(file1, file2):
    """
    Compare two CSV files column by column, considering only digits unaffected by rounding.
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Ensure both dataframes have the same columns
    if set(df1.columns) != set(df2.columns):
        raise ValueError("The two CSV files have different columns and cannot be compared.")

    comparison_results = {}
    for column in df1.columns:
        if column in df2.columns:
            if pd.api.types.is_numeric_dtype(df1[column]) and pd.api.types.is_numeric_dtype(df2[column]):
                # Compare rounded values to 6 decimal places
                comparison_results[f"identical_{column}"] = df1[column].round(6).equals(df2[column].round(6))
            else:
                # Compare non-numeric columns directly
                comparison_results[f"identical_{column}"] = df1[column].equals(df2[column])
        else:
            comparison_results[f"identical_{column}"] = False

    return comparison_results

def find_matching_pairs():
    matching_pairs = []
    for file_name in os.listdir(ORIG_RESULTS_DIR):
        if file_name.endswith("_results.csv"):
            orig_file_path = os.path.join(ORIG_RESULTS_DIR, file_name)
            repro_file_path = os.path.join(CSV_DIR, f"repro_{file_name}")
            if os.path.exists(repro_file_path):
                matching_pairs.append((repro_file_path, orig_file_path))
    return matching_pairs

def check_log_file(log_file_name, log_dir):
    log_file_path = os.path.join(log_dir, log_file_name)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
            lines = log_file.readlines()
            if len(lines) > 5 and "Your do-file runs without errors." in lines[5]:
                return True
            else:
                return False
    return None

def move_files_to_checked(files, source_dir):
    checked_dir = os.path.join(source_dir, "checked")
    if not os.path.exists(checked_dir):
        os.makedirs(checked_dir)
    for file in files:
        os.rename(os.path.join(source_dir, file), os.path.join(checked_dir, file))
        print(f"Moved {file} to {checked_dir}")

def main():
    # Execute the new functionality first
    round_csv_numbers()

    matching_pairs = find_matching_pairs()
    results = []

    print("Matched pairs:")
    for repro_file, orig_file in matching_pairs:
        repro_file_name = os.path.basename(repro_file)
        orig_file_name = os.path.basename(orig_file)
        print(f"Repro file: {repro_file_name} <-> Orig file: {orig_file_name}")
        comparison_results = compare_csv(repro_file, orig_file)
        result = {
            "repro_file": repro_file_name,
            "orig_file": orig_file_name
        }
        result.update(comparison_results)
        results.append(result)

        # Check if the results are reproduced
        reproduced = all(comparison_results.values())

        # Create summary JSON
        summary = {
            "reproduced": reproduced,
            "succeededFor5Percent": None,
            "succeededFor95Percent": None
        }

        # Save summary JSON
        summary_file_name = orig_file_name.replace("_results.csv", ".json")
        summary_file_path = os.path.join(SUMMARY_DIR, summary_file_name)
        with open(summary_file_path, 'w') as summary_file:
            json.dump(summary, summary_file, indent=4)
        print(f"Summary saved to {summary_file_path}")

    print(f"Total number of matched files: {len(matching_pairs)}")

    # Check log files for errors for all log files
    for file_name in os.listdir(ORIG_RESULTS_DIR):
        log_file_name_5 = file_name.replace("_results.csv", "_5%.log")
        log_file_name_95 = file_name.replace("_results.csv", "_95%.log")
        succeeded_for_5_percent = check_log_file(log_file_name_5, LOG_DIR_RT)
        succeeded_for_95_percent = check_log_file(log_file_name_95, LOG_DIR_PC)

        # Create or update summary JSON
        summary_file_name = file_name.replace("_results.csv", ".json")
        summary_file_path = os.path.join(SUMMARY_DIR, summary_file_name)
        if os.path.exists(summary_file_path):
            with open(summary_file_path, 'r') as summary_file:
                summary = json.load(summary_file)
        else:
            summary = {
                "reproduced": False,
                "succeededFor5Percent": None,
                "succeededFor95Percent": None
            }
        summary["succeededFor5Percent"] = succeeded_for_5_percent
        summary["succeededFor95Percent"] = succeeded_for_95_percent
        with open(summary_file_path, 'w') as summary_file:
            json.dump(summary, summary_file, indent=4)
        print(f"Updated summary saved to {summary_file_path}")

    # Move all repro files to the "checked" subfolder
    repro_files = [file for file in os.listdir(CSV_DIR) if file.startswith("repro_") and file.endswith(".csv")]
    move_files_to_checked(repro_files, CSV_DIR)

    # Move all orig files to the "checked" subfolder
    orig_files = [file for file in os.listdir(ORIG_RESULTS_DIR) if file.endswith("_results.csv")]
    move_files_to_checked(orig_files, ORIG_RESULTS_DIR)

    # Move repro results from 95% sample to the "lib" subfolder
    repro_files_pc = [file for file in os.listdir(CSV_DIR_PC) if file.startswith("repro_") and file.endswith(".csv")]
    move_files_to_checked(repro_files_pc, CSV_DIR_PC)

if __name__ == "__main__":
    main()