import os

def process_log_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
    
    error_lines = []
    cap_lines = []
    
    for i in range(len(lines)):
        if lines[i].strip().startswith("r("):
            error_lines.append(str(i + 8))
        elif lines[i].strip().startswith("cap") or lines[i].strip().startswith("capture"):
            cap_lines.append(str(i + 8))
    
    if error_lines:
        error_message = f"ATTENTION: RUNNING YOUR do-file PRODUCES ERRORS, see lines {', '.join(error_lines)}.\n"
    elif cap_lines:
        error_message = f"ATTENTION: It appears as if you use a cap or capture command. We cannot verify, whether your script runs without errors., see lines {', '.join(cap_lines)}.\n"
    else:
        error_message = "Your do-file runs without errors.\n"
    
    intro_lines = [
        "\n",
        "This is the log-file generated when running your do-file with the 5%-sample of the SOEP data.\n",
        "\n",
        "\n",
        "\n",
        error_message,
        '\n'
    ]
    
    result_lines = intro_lines + lines  # Add intro lines and keep all subsequent lines as is

    with open(output_path, 'w') as outfile:
        outfile.writelines(result_lines)
    print(f"Created processed log file: {output_path}")

def move_log_file_to_lib(log_file_path):
    lib_dir = os.path.join(os.path.dirname(log_file_path), 'lib')
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)
    new_path = os.path.join(lib_dir, os.path.basename(log_file_path))
    os.rename(log_file_path, new_path)
    print(f"Moved {log_file_path} to {new_path}")

def main():
    log_dir = 'ManyDaughters_RT_AnalysisPackage/log'
    processed_dir = os.path.join(log_dir, 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            input_path = os.path.join(log_dir, filename)
            output_filename = filename.replace('.log', '_5%.log')
            output_path = os.path.join(processed_dir, output_filename)
            process_log_file(input_path, output_path)
            move_log_file_to_lib(input_path)

if __name__ == "__main__":
    main()