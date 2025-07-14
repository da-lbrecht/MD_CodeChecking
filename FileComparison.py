#!/usr/bin/env python3
"""
File Comparison Tool
Compares two text files and reports differences with line numbers.
"""

import os
import sys
from difflib import unified_diff


def read_file(file_path):
    """
    Read a file and return its lines.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        list: List of lines from the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")


def compare_files(file1_path, file2_path):
    """
    Compare two files and return their differences.
    
    Args:
        file1_path (str): Path to first file
        file2_path (str): Path to second file
        
    Returns:
        tuple: (are_identical, differences_list)
    """
    try:
        lines1 = read_file(file1_path)
        lines2 = read_file(file2_path)
        
        # Check if files are identical
        if lines1 == lines2:
            return True, []
        
        # Generate unified diff
        diff = list(unified_diff(
            lines1, 
            lines2, 
            fromfile=f"File 1: {os.path.basename(file1_path)}",
            tofile=f"File 2: {os.path.basename(file2_path)}",
            lineterm=''
        ))
        
        return False, diff
        
    except Exception as e:
        raise Exception(f"Error comparing files: {e}")


def display_differences(diff_lines):
    """
    Display the differences in a readable format.
    
    Args:
        diff_lines (list): List of diff lines from unified_diff
    """
    print("\n" + "="*60)
    print("DIFFERENCES FOUND:")
    print("="*60)
    
    for line in diff_lines:
        line = line.rstrip()
        if line.startswith('+++') or line.startswith('---'):
            print(f"\n{line}")
        elif line.startswith('@@'):
            print(f"\n{line}")
        elif line.startswith('+'):
            print(f"  {line}")  # Added lines
        elif line.startswith('-'):
            print(f"  {line}")  # Removed lines
        elif not line.startswith('\\'):
            print(f"  {line}")  # Context lines


def get_file_path(prompt):
    """
    Get a valid file path from user input.
    
    Args:
        prompt (str): Prompt message for user
        
    Returns:
        str: Valid file path
    """
    while True:
        file_path = input(prompt).strip()
        
        if not file_path:
            print("Please enter a valid file path.")
            continue
            
        # Remove quotes if present
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        elif file_path.startswith("'") and file_path.endswith("'"):
            file_path = file_path[1:-1]
        
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"File not found: {file_path}")
            print("Please enter a valid file path.")


def main():
    """
    Main function to run the file comparison tool.
    """
    print("="*60)
    print("FILE COMPARISON TOOL")
    print("="*60)
    print("This tool compares two text files and shows differences.")
    print()
    
    try:
        # Get file paths from user
        file1_path = get_file_path("Enter the path to the first file: ")
        file2_path = get_file_path("Enter the path to the second file: ")
        
        print(f"\nComparing files:")
        print(f"  File 1: {file1_path}")
        print(f"  File 2: {file2_path}")
        
        # Compare files
        are_identical, differences = compare_files(file1_path, file2_path)
        
        if are_identical:
            print("\n" + "="*60)
            print("✓ FILES ARE IDENTICAL")
            print("="*60)
            print("The two files have exactly the same content.")
        else:
            display_differences(differences)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()