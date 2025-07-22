import os
import glob

def find_matching_files(filename_string, base_directories):
    """Find all files containing the given string in filename, excluding .do files and .csv files that start with the string"""
    matching_files = []
    
    for base_dir in base_directories:
        if os.path.exists(base_dir):
            # Search pattern: *string* in all subdirectories
            pattern = os.path.join(base_dir, "**", f"*{filename_string}*")
            files = glob.glob(pattern, recursive=True)
            
            # Filter out .do files and .csv files that start with the string, only include actual files (not directories)
            filtered_files = []
            for f in files:
                if os.path.isfile(f) and not f.endswith('.do'):
                    filename = os.path.basename(f)
                    # Exclude .csv files that start with the filename string
                    if f.endswith('.csv') and filename.startswith(filename_string):
                        continue
                    filtered_files.append(f)
            matching_files.extend(filtered_files)
    
    return matching_files

def find_do_and_csv_files(filename_string, base_directories):
    """Find all .do files containing the string and .csv files starting with the string"""
    special_files = []
    
    for base_dir in base_directories:
        if os.path.exists(base_dir):
            # Search pattern for .do files: *string*.do in all subdirectories
            do_pattern = os.path.join(base_dir, "**", f"*{filename_string}*.do")
            do_files = glob.glob(do_pattern, recursive=True)
            
            # Search pattern for .csv files starting with string: string*.csv in all subdirectories
            csv_pattern = os.path.join(base_dir, "**", f"{filename_string}*.csv")
            csv_files = glob.glob(csv_pattern, recursive=True)
            
            # Only include actual files (not directories)
            filtered_do_files = [f for f in do_files if os.path.isfile(f)]
            filtered_csv_files = [f for f in csv_files if os.path.isfile(f)]
            special_files.extend(filtered_do_files)
            special_files.extend(filtered_csv_files)
    
    return special_files

def process_files(filename_string, base_directories):
    # Find matching files
    print(f"\nSearching for files containing '{filename_string}'...")
    print("Searching in directories:")
    for base_dir in base_directories:
        if os.path.exists(base_dir):
            print(f"  ✓ {base_dir}")
        else:
            print(f"  ✗ {base_dir} (not found)")
    print()
    
    matching_files = find_matching_files(filename_string, base_directories)
    
    if not matching_files:
        print("No matching files found.")
    else:
        # Display found files
        print(f"\nFound {len(matching_files)} matching files:")
        for file_path in matching_files:
            print(f"  {file_path}")
        
        # Ask for confirmation
        confirmation = input(f"\nDo you want to delete these {len(matching_files)} files? (y/n): ").strip().lower()
        
        if confirmation == 'y':
            deleted_count = 0
            for file_path in matching_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    deleted_count += 1
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
            
            print(f"\nSuccessfully deleted {deleted_count} out of {len(matching_files)} files.")
        else:
            print("Operation cancelled. No files deleted.")
    
    # Handle .do files and .csv files starting with the string
    print(f"\nSearching for .do files containing '{filename_string}' and .csv files starting with '{filename_string}'...")
    special_files = find_do_and_csv_files(filename_string, base_directories)
    
    if not special_files:
        print("No matching .do files or .csv files starting with the string found.")
    else:
        # Display found .do and .csv files
        print(f"\nFound {len(special_files)} matching .do files and .csv files starting with the string:")
        for file_path in special_files:
            print(f"  {file_path}")
        
        # Ask for confirmation to move .do and .csv files
        confirmation = input(f"\nDo you want to move these {len(special_files)} .do and .csv files one directory up? (y/n): ").strip().lower()
        
        if confirmation == 'y':
            moved_count = 0
            for file_path in special_files:
                try:
                    parent_dir = os.path.dirname(os.path.dirname(file_path))
                    filename = os.path.basename(file_path)
                    new_path = os.path.join(parent_dir, filename)
                    
                    # Check if destination already exists
                    if os.path.exists(new_path):
                        print(f"Skipped {file_path}: destination already exists")
                        continue
                    
                    os.rename(file_path, new_path)
                    print(f"Moved: {file_path} -> {new_path}")
                    moved_count += 1
                except OSError as e:
                    print(f"Error moving {file_path}: {e}")
            
            print(f"\nSuccessfully moved {moved_count} out of {len(special_files)} .do and .csv files.")
        else:
            print("Move operation cancelled. No .do or .csv files moved.")
    
    print("\nOperation completed.")

def main():
    while True:
        # Define the directories to search
        base_directories = [
            "ManyDaughters_PC_AnalysisPackage_95",
            "ManyDaughters_RT_AnalysisPackage"
        ]
        
        # Get filename string from user
        filename_string = input("Enter filename string: ").strip()
        
        if not filename_string:
            print("No filename string provided. Exiting.")
            break
        
        process_files(filename_string, base_directories)
        
        # Ask if user wants to continue
        continue_choice = input("\nDo you want to reset another check? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("Exiting application.")
            break

if __name__ == "__main__":
    main()
