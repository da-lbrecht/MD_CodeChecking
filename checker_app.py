import requests
import os

# Constants
GITHUB_REPO = "ManyDaughters/RT_uploads"
DIRECTORY_PATH = "do-files"
DOWNLOAD_DIR = "RT_StataCode"  # Local directory to store downloaded files

# Create a local download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Function to get the contents of the specified directory in the GitHub repo
def get_github_files(repo, directory):
    url = f"https://api.github.com/repos/{repo}/contents/{directory}"
    response = requests.get(url)
    return response.json()

# Function to download a file from GitHub
def download_file(url, file_name):
    response = requests.get(url)
    with open(os.path.join(DOWNLOAD_DIR, file_name), 'wb') as f:
        f.write(response.content)

def main():
    try:
        files = get_github_files(GITHUB_REPO, DIRECTORY_PATH)
        
        for file in files:
            file_name = file['name']
            file_download_url = file['download_url']
            
            # Check if the file already exists in the local directory
            local_file_path = os.path.join(DOWNLOAD_DIR, file_name)
            if not os.path.exists(local_file_path):
                print(f"Downloading {file_name}...")
                download_file(file_download_url, file_name)
            else:
                print(f"{file_name} already exists. Skipping download.")

        print("Download complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()