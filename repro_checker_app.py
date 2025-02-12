import os
import pandas as pd

# Constants
ROOT_DIR = os.path.abspath(".")
CSV_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "out")  # Local directory where results from the reproduction check are stored
ORIG_RESULTS_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "results")  # Local directory where submitted results are stored
CHECK_RESULTS_DIR = os.path.join(ROOT_DIR, "ManyDaughters_RT_AnalysisPackage", "repro_check")  # Local directory to store results of computational reproducibility check

# Ensure the check results directory exists
if not os.path.exists(CHECK_RESULTS_DIR):
    os.makedirs(CHECK_RESULTS_DIR)

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

    print(f"Total number of matched files: {len(matching_pairs)}")

    # Save the results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(CHECK_RESULTS_DIR, "repro_check.csv"), index=False)
    print(f"Reproducibility check results saved to {os.path.join(CHECK_RESULTS_DIR, 'repro_check.csv')}")

if __name__ == "__main__":
    main()