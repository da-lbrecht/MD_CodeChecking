import os
import pandas as pd
import json

# Constants
ROOT_DIR = os.path.abspath(".")
CSV_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "out")  # Local directory where results from the reproduction check are stored
ORIG_RESULTS_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "results")  # Local directory where submitted results are stored
LOG_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "log", "processed")  # Local directory to store processed log files
SUMMARY_DIR = os.path.join(ROOT_DIR, "summary")  # Local directory to store summary JSON files

# Ensure the summary directory exists
if not os.path.exists(SUMMARY_DIR):
    os.makedirs(SUMMARY_DIR)

def compare_csv(file1, file2):
    # Read the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Compare the dataframes column by column
    comparison_results = {}
    for column in df1.columns:
        if column in df2.columns:
            comparison_results[f"identical_{column}"] = df1[column].equals(df2[column])
        else:
            comparison_results[f"identical_{column}"] = False

    return comparison_results

def find_matching_pairs():
    matching_pairs = []
    for file_name in os.listdir(CSV_DIR):
        if file_name.startswith("repro_") and file_name.endswith(".csv"):
            orig_file_name = file_name[len("repro_"):]
            orig_file_path = os.path.join(ORIG_RESULTS_DIR, orig_file_name)
            repro_file_path = os.path.join(CSV_DIR, file_name)
            if os.path.exists(orig_file_path):
                matching_pairs.append((repro_file_path, orig_file_path))
    return matching_pairs

def check_log_file(log_file_name):
    log_file_path = os.path.join(LOG_DIR, log_file_name)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
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

        # Check log file for errors
        log_file_name = orig_file_name.replace("_results.csv", "_5%.log")
        succeeded_for_5_percent = check_log_file(log_file_name)

        # Check if the results are reproduced
        reproduced = all(comparison_results.values())

        # Create summary JSON
        summary = {
            "succeededFor5Percent": succeeded_for_5_percent,
            "succeededFor95Percent": None,
            "reproduced": reproduced
        }

        # Save summary JSON
        summary_file_name = orig_file_name.replace("_results.csv", ".json")
        summary_file_path = os.path.join(SUMMARY_DIR, summary_file_name)
        with open(summary_file_path, 'w') as summary_file:
            json.dump(summary, summary_file, indent=4)
        print(f"Summary saved to {summary_file_path}")

    print(f"Total number of matched files: {len(matching_pairs)}")

    # Move files to the "checked" subfolder
    repro_files = [os.path.basename(pair[0]) for pair in matching_pairs]
    orig_files = [os.path.basename(pair[1]) for pair in matching_pairs]
    move_files_to_checked(repro_files, CSV_DIR)
    move_files_to_checked(orig_files, ORIG_RESULTS_DIR)

if __name__ == "__main__":
    main()