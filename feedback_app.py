import os

def process_log_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
    
    error_lines = []
    result_lines = [
        '\n',
        'This is the log-file generated when running your do-file on the 95%-sample of the SOEP data.\n',
        'All output has been censored.\n',
        '\n',
        'We have spotted error messages in lines\n',
        '\n'
    ] + ['\n'] * (len(lines) + 1)  # Initialize with blank lines after the first 5 lines
    
    for i in range(len(lines)):
        if lines[i].startswith(". *") or "r(" in lines[i]:
            if "r(" in lines[i]:
                error_lines.append(str(i + 1))
            start_index = max(0, i - 3)
            for j in range(start_index, i + 1):
                if j + 6 < len(result_lines):
                    result_lines[j + 6] = lines[j]  # Offset by 6 to account for the added lines
    
    result_lines[4] = 'We have spotted error messages in lines ' + ', '.join(error_lines) + '\n'
    
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
