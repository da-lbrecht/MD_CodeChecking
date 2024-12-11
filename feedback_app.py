import os

def process_log_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
    
    error_lines = []
    
    for i in range(len(lines)):
        if "r(" in lines[i]:
            error_lines.append(str(i + 7))
    
    if error_lines:
        error_message = f"ATTENTION: RUNNING YOUR do-file PRODUCES ERRORS, see lines {', '.join(error_lines)}.\n"
    else:
        error_message = "Your do-file runs without errors.\n"
    
    intro_lines = [
        "\n",
        "This is the log-file generated when running your do-file with the 95%-sample of the SOEP data.\n",
        "\n",
        "All output has been censored. Commented lines, and passages that produce an error message are still visible.\n",
        "\n",
        error_message,
        '\n'
    ]
    
    result_lines = intro_lines + lines[:24]  # Add intro lines and keep the first 24 lines as is
    
    for i in range(24, len(lines)):
        if lines[i].startswith(". *") or "r(" in lines[i] or \
           (i + 1 < len(lines) and "r(" in lines[i + 1]) or \
           (i + 2 < len(lines) and "r(" in lines[i + 2]):
            result_lines.append(lines[i])
        else:
            result_lines.append('\n')  # Blank the line
    
    with open(output_path, 'w') as outfile:
        outfile.writelines(result_lines)

def main():
    log_dir = 'ManyDaughters_RT_AnalysisPackage/log'
    censored_dir = os.path.join(log_dir, 'censored')
    os.makedirs(censored_dir, exist_ok=True)
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            input_path = os.path.join(log_dir, filename)
            output_filename = filename.replace('.log', '_censored.log')
            output_path = os.path.join(censored_dir, output_filename)
            process_log_file(input_path, output_path)

if __name__ == "__main__":
    main()