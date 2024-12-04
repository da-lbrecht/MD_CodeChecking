import os

def process_log_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()
    
    result_lines = []
    for i in range(len(lines)):
        if lines[i].startswith("r("):
            start_index = max(0, i - 5)
            result_lines.extend(lines[start_index:i + 1])
    
    with open(output_path, 'w') as outfile:
        outfile.writelines(result_lines)

def main():
    log_dir = 'ManyDaughters_RT_AnalysisPackage/log'
    censored_dir = os.path.join(log_dir, 'censored')
    os.makedirs(censored_dir, exist_ok=True)
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            input_path = os.path.join(log_dir, filename)
            output_path = os.path.join(censored_dir, filename)
            process_log_file(input_path, output_path)

if __name__ == "__main__":
    main()
