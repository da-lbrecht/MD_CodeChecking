import sys

file1 = input("Enter path to first file: ").strip()
file2 = input("Enter path to second file: ").strip()

try:
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
except Exception as e:
    print(f"Error reading files: {e}")
    sys.exit(1)

if lines1 == lines2:
    print("Files are identical.")
else:
    min_len = min(len(lines1), len(lines2))
    for i in range(min_len):
        if lines1[i] != lines2[i]:
            print(f"Files differ at line {i+1}:")
            print(f"File 1: {lines1[i].rstrip()}")
            print(f"File 2: {lines2[i].rstrip()}")
            break
    else:
        if len(lines1) != len(lines2):
            print(f"Files differ in length. File 1 has {len(lines1)} lines, File 2 has {len(lines2)} lines.")
