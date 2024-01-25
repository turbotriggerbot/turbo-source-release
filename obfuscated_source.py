


import mss
import numpy as np
from PIL import Image
import PIL.ImageGrab
import PIL.Image
import time
import colorsys
import sys
import keyboard
import tkinter as tk
import winsound
import requests
import wmi
import threading

import os
import requests
import wmi
import numpy as np



S_WIDTH , S_HEIGHT = (PIL.ImageGrab.grab().size)
colorSelected = 0



latency = 220
hold = 0
toggle = True
strafeToggle = False
grabzone = 4
mode = []
selectedMode = 0



VALID = False
TYPE = "1"
url = "https://phenomenal-pavlova-61f19a.netlify.app/.netlify/functions/mode-validation"  
AUTHurl = "https://phenomenal-pavlova-61f19a.netlify.app/.netlify/functions/key-validation"  # Replace with your actual Netlify function endpoint
canModify = False






def get_system_uuid():
    try:
        c = wmi.WMI()
        system_uuid = c.Win32_ComputerSystemProduct()[0].UUID
        return system_uuid
    except Exception as e:
        print(f"Error: {e}")
        return None

user_input_key = input("Enter your key: ")
uuid = get_system_uuid()

payload = {"key": user_input_key, "uuid": uuid}

response = requests.post(AUTHurl, json=payload)

if response.status_code == 200:
    AUTHresult = response.json()
    if AUTHresult.get("valid"):
        VALID = True
        print("Key is valid.\n")
        if AUTHresult.get("type") == '1' :
            print("continuing in trial mde\n")
            TYPE = "1"
        if AUTHresult.get("type") == '2' :
            print("continuing in standard mode\n")
            TYPE = "2"
        if AUTHresult.get("type") == '3' :
            print("continuing in custom mode\n")
            TYPE = "3"
          
        
    else:
        VALID = False
        print("Invalid UUID. Exiting the app.")
        time.sleep(5)
        exit()
        sys.exit("exiting")
else:
    print("Invalid key or UUID. Exiting the app.")
    time.sleep(5)
    print(f"Error: {response.status_code}, {response.text}")
    exit()
    sys.exit("exiting")




def send_web_request(request_type_to_send , config_to_send) : 
    global result   , canModify
    result = config_to_send
    payload = {"user": username , "config" : config_to_send , "requestType" : request_type_to_send  }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        if(username != "public") :
            canModify = True
 #       print(result)
    elif response.status_code == 204:
        print("saved successfully")
    else:

        #user isnt registered 
        print(f"{response.text}")
        # fetch data for public user
        payload = {"user": "public"  ,  "config" : config_to_send , "requestType" : request_type_to_send  }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
        else : 
            print("couldnt fetch public data")




def modify_settings(config):
    while True:
        
        # Prompt the user to select a mode
        print("Available modes:")
        for i, mode in enumerate(config['modes'], start=1):
            print(f"{i}. {mode}")

        print("0. Exit")
        selected_mode_index = input("Select a mode (enter a number): ")

        if selected_mode_index == '0':
            break

        try:
            selected_mode_index = int(selected_mode_index)
            if 1 <= selected_mode_index <= len(config['modes']):
                selected_mode = list(config['modes'])[selected_mode_index - 1]
            else:
                print("Invalid mode index. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Prompt the user to select a field to modify
        print("\nAvailable fields to modify:")
        print("1. Hotkey")
        print("2. Latency")
        print("3. Hold")

        selected_field = input("Select a field to modify (enter a number) or 'exit' to quit: ").lower()

        if selected_field == 'exit':
            break

        # Check if the selected field is valid
        if selected_field not in ['1', '2', '3']:
            print("Invalid selection. Please try again.")
            continue

        # Prompt the user for the new value
        new_value = input(
            f"Enter the new value for {config['modes'][selected_mode]['name']}'s "
            f"{['Hotkey', 'Latency', 'Hold'][int(selected_field) - 1]}: "
        )

        # Update the selected field
        if selected_field == '1':
            config['modes'][selected_mode]['hotkey'] = new_value
        elif selected_field == '2':
            config['modes'][selected_mode]['latency'] = int(new_value)
        elif selected_field == '3':
            config['modes'][selected_mode]['hold'] = int(new_value)


        clear = lambda: os.system('cls')
        clear()
        print(f"updated successfully for {selected_mode}!\n")
      #  print(config)
        send_web_request("save" , config)

def print_modes_and_fields(config):
    # Print modes and their modifiable fields
    for mode, details in config['modes'].items():
        print(f"\nMode: {mode}")
        print("Modifiable Fields:")
        print(f"1. Hotkey: {details['hotkey']}")
        print(f"2. Latency: {details['latency']}")
        print(f"3. Hold: {details['hold']}")


if (TYPE == '3'):
    username = input("enter username :  ")
    send_web_request("load" , "null_config")
    while 1 == 1 :

        cmd = input("enter : \n   1 . to start\n   2 . to modify config\n   3 . to show current config\n-> ")
        if cmd == '1' :
            clear = lambda: os.system('cls')
            clear()
            break

        elif cmd == '2' :
            clear = lambda: os.system('cls')
            clear()
            if not canModify:
                print("can't modify the public user profile") 
                continue
            modify_settings(result)
            
        elif cmd == '3' :
            clear = lambda: os.system('cls')
            clear()
            print_modes_and_fields(result)

elif TYPE == '2' or TYPE == "1" :
    username = "public"
    send_web_request("load" , "null_config")


print("running ! ")


PURPLE_H_UPPER, PURPLE_S_UPPER, PURPLE_V_UPPER = (
        result["colors"]["purple_h_upper"],
        result["colors"]["purple_s_upper"],
        result["colors"]["purple_v_upper"]
        )
PURPLE_H_LOWER, PURPLE_S_LOWER, PURPLE_V_LOWER = (
        result["colors"]["purple_h_lower"],
        result["colors"]["purple_s_lower"],
        result["colors"]["purple_v_lower"]
        )

YELLOW_H_UPPER, YELLOW_S_UPPER, YELLOW_V_UPPER = (
        result["colors"]["yellow_h_upper"],
        result["colors"]["yellow_s_upper"],
        result["colors"]["yellow_v_upper"]
        )
YELLOW_H_LOWER, YELLOW_S_LOWER, YELLOW_V_LOWER = (
        result["colors"]["yellow_h_lower"],
        result["colors"]["yellow_s_lower"],
        result["colors"]["yellow_v_lower"]
        )


RED_H_UPPER, RED_S_UPPER, RED_V_UPPER  , RED_H_UPPER2= (
        result["colors"]["red_h_upper"],
        result["colors"]["red_s_upper"],
        result["colors"]["red_v_upper"],
        result["colors"]["red_h_upper2"]
        )
RED_H_LOWER, RED_S_LOWER, RED_V_LOWER = (
        result["colors"]["red_h_lower"],
        result["colors"]["red_s_lower"],
        result["colors"]["red_v_lower"]
        )





def rgb_to_hsv_vectorized(rgb_array):
    def rgb_to_hsv(rgb):
        r, g, b = rgb
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return np.round(h * 360), np.round(s * 100), np.round(v * 100)

    return np.apply_along_axis(rgb_to_hsv, -1, rgb_array)
def approx_vectorized(rgb_array, color):
    rgb_array = np.array(rgb_array) / 255.0
    hsv_array = rgb_to_hsv_vectorized(rgb_array)
    
    h, s, v = np.moveaxis(hsv_array, -1, 0)
    
    if color == 0:
        return np.logical_and.reduce([
            YELLOW_H_LOWER <= h, h <= YELLOW_H_UPPER,
            YELLOW_S_LOWER <= s, s <=YELLOW_S_UPPER,
            YELLOW_V_LOWER <= v, v <= YELLOW_V_UPPER
        ])
    elif color == 1:
        return np.logical_and.reduce([
            PURPLE_H_LOWER  <= h, h <= PURPLE_H_UPPER ,
            PURPLE_S_LOWER  <= s, s <= PURPLE_S_UPPER ,
            PURPLE_V_LOWER  <= v, v <= PURPLE_V_UPPER 
        ])
    elif color == 2:
        return np.logical_and.reduce([

            (RED_H_LOWER <= h) | (h <= RED_H_UPPER2) | (RED_H_LOWER <= h),  
            RED_S_LOWER  <= s, s <= RED_S_UPPER,
            RED_V_LOWER <= v, v <= RED_V_UPPER
        ])



def grab():    
    global grabzone
    with mss.mss() as sct:
        bbox = (
            int(S_WIDTH/2 - grabzone     ),
            int(S_HEIGHT/2 - (grabzone * 3)   ),
            int(S_WIDTH/2 + grabzone    ),  # Centered adjustment for the height
            int(S_HEIGHT/2 )#+ grabzone )
        )
        sct_img = sct.grab(bbox)

        return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def checkIfScoped() :
    with mss.mss() as sct:
        bbox = (
            int(S_WIDTH/2 - 1     ),
            int(S_HEIGHT/2 - 1   ),
            int(S_WIDTH/2    ),  # Centered adjustment for the height
            int(S_HEIGHT/2 )#+ grabzone )
        )
        sct_img = sct.grab(bbox)

        img =  PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    for y in range(1):
        for x in range(1):
            # Get the RGB values of the current pixel
            pixel = img.getpixel((x, y))

            if all(value >= 200 for value in pixel):
                return True
    return False


def mainthread():
    global toggle
    S_WIDTH , S_HEIGHT = (PIL.ImageGrab.grab().size)
    
    #keyboard.add_hotkey('ctrl+alt', toggleFunc)


    def click(latency , hold):
        global found
        global selectedMode
 
        if selectedMode == 1 :
            if not checkIfScoped() :
                return
        if (strafeToggle):

            if not (keyboard.is_pressed('d') or keyboard.is_pressed('a') or keyboard.is_pressed('w') or keyboard.is_pressed('q') or  keyboard.is_pressed("s") or (keyboard.is_pressed("z") ) ) :
                keyboard.press("l")
                time.sleep(hold / 1000)
                keyboard.release("l")
                found = True          

            elif (keyboard.is_pressed('d') and keyboard.is_pressed('q')) :
                keyboard.press("l")
                time.sleep(hold / 1000)
                keyboard.release("l")
                found = True          
        else :
                keyboard.press("l")
                time.sleep(hold / 1000)
                keyboard.release("l")


    sent_warning_text = False
    while True:
        # this is a new toggler fucntion base on the db
        if(keyboard.is_pressed(result["misc"]["toggle_hotkey"] )):
            toggleFunc()
        if not toggle :
            time.sleep(0.01)
            continue

        if result["misc"]["hold_to_toggle"] == "yes" : 
            if not sent_warning_text :
                print("WARNING : THE BOT IS SET TO SHOOT WHEN HODLDING MODE WITH THE KEY : " ,result["misc"]["hold_key"] )
                sent_warning_text = True
            if not keyboard.is_pressed(result["misc"]["hold_key"]) :
                time.sleep(0.05)
                continue
 

        pmap = grab()
        found = False
    
        try:
            rgb_array = np.array(pmap)
            mask = approx_vectorized(rgb_array, colorSelected)
            found = np.any(mask)
            if found:
                # Extract coordinates where the condition is met
                #y, x = np.where(mask)
                click(latency, hold)
                time.sleep(latency / 1000)
        except IndexError:
            pass
            


thread = threading.Thread(target=mainthread, daemon=True)




if VALID:
    thread.start()




def toggleFunc():

    switch.toggle()

def mode_button_click(mode):
    global latency
    global hold
    global selectedMode
    print(mode)
    if mode == "operator" :
        selectedMode = 1
        
    else:
        selectedMode = 0
  #  print("selected mode  :" , selectedMode)
    if result["misc"]["mute"] == "no" : 
        winsound.Beep(380,100)
 
    for key in tkinter_elements:
  
        tkinter_elements[key].configure(bg_color="transparent")
        tkinter_elements[key].configure(fg_color="#5999ff")
      
    tkinter_elements[mode].configure(bg_color="transparent")
    tkinter_elements[mode].configure(fg_color="#032d3c")
    latency = result["modes"][mode]["latency"]
    hold = result["modes"][mode]["hold"]
    
   



#def mode_button_click(mode_name):
#    # Your logic for handling mode button clicks
#    print(f"Mode button clicked: {mode_name}")

def hotkey_listener(hotkey_combination, mode_name):
    while True:
        keyboard.wait(hotkey_combination)
        mode_button_click(mode_name)
        winsound.Beep(440, 75)

# Create a thread for each hotkey
hotkey_threads = []
for key in result["modes"]:
    hotkey_combination = result["modes"][key]["hotkey"]
    mode_name = result["modes"][key]["name"]

    if hotkey_combination != "null":
        hotkey_thread = threading.Thread(target=hotkey_listener, args=(hotkey_combination, mode_name), daemon=True)
        hotkey_threads.append(hotkey_thread)
        hotkey_thread.start()

# Keep the program running


# Keep the program runni


def color_button_click(color):
    global colorSelected
    # Implement the color button function here
    if color == "Yellow" :
        yellow.configure(bg_color="transparent")
        yellow.configure(fg_color="yellow")
        yellow.configure(text_color="black")

        purple.configure(fg_color="#5999ff")
        purple.configure(bg_color="transparent")
        purple.configure(text_color="white")
        red.configure(fg_color="#5999ff")
        red.configure(bg_color="transparent")
        red.configure(text_color="white")
              
        colorSelected =0

    elif color == "Purple":
        purple.configure(bg_color="transparent")
        purple.configure(fg_color="pink")
        purple.configure(text_color="black")

        yellow.configure(fg_color="#5999ff")
        yellow.configure(bg_color="transparent")
        yellow.configure(text_color="white")
        red.configure(fg_color="#5999ff")
        red.configure(bg_color="transparent")
        red.configure(text_color="white")
           

        colorSelected =1

    elif color == "Red":
        red.configure(bg_color="transparent")
        red.configure(fg_color="red")
        red.configure(text_color="black")

        purple.configure(fg_color="#5999ff")
        purple.configure(bg_color="transparent")
        purple.configure(text_color="white")


        yellow.configure(fg_color="#5999ff")
        yellow.configure(bg_color="transparent")
        yellow.configure(text_color="white")

        colorSelected =2


    pass

def decrement_box_size():
    global grabzone
    if grabzone > 1:
        grabzone-=1

    box_size_entry.configure(text=str(grabzone))
    

def increment_box_size():
    global grabzone
    if grabzone < 20:
        grabzone+=1

    box_size_entry.configure(text=str(grabzone))
    

    pass
    
def use_custom_res( ):
    global S_WIDTH 
    global S_HEIGHT
    global usingCustomRes
 
    if usingCustomRes:   
        S_WIDTH, S_HEIGHT = PIL.ImageGrab.grab().size
    else:
        pass

    usingCustomRes = not usingCustomRes

    try:
        
        
        width = int(custom_w.get())
        height = int(custom_h.get())
    
        S_WIDTH = width
        S_HEIGHT = height
        print( width , height)
    except ValueError:
       
        print("Invalid entry values. Please enter valid integers for width and height.")
    



usingCustomRes = True
import customtkinter
from typing import Union, Callable

# Create the main Tkinter window


if VALID :
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.title("Turbo")
    app.attributes('-topmost', True)
    app.option_add('*Font', ("Nunito", 14, 'bold'))
    app.geometry("320x650")
    app.grid_columnconfigure((0, 1, 2), weight=1)


    toggle_text = customtkinter.CTkLabel(app, text="Toggle", font=('consola', 16, 'bold'))

    def switch_event():
        global toggle
        global switch_var
        

        toggle = not toggle
        if toggle : 
            if result["misc"]["mute"] == "no" : 
                winsound.Beep(600, 300)  # Frequency: 1000 Hz, Duration: 500 milliseconds
        else : 
            if result["misc"]["mute"] == "no" : 
                winsound.Beep(300, 300)  # Frequency: 300 Hz, Duration: 1000 milliseconds
        

        
        
    switch_var = customtkinter.StringVar(value="on")
    switch = customtkinter.CTkSwitch(app, text="", command=switch_event,
                                     variable=switch_var, onvalue="on", offvalue="off", progress_color="#00FF00")
                                     

    # Weapons selection text
    wpn_text = customtkinter.CTkLabel(app, text="mode", font=('consola', 16, 'bold'))

    # Weapons selection checkboxes

    tkinter_elements = {}
    for key , value in result["modes"].items():
    #    code = result["modes"][key]["code"]
        element_name = result["modes"][key]["name"]        

        code =  element_name
        #print(result)
        tkinter_elements[element_name] =  customtkinter.CTkButton(app, text=element_name  , 
        command=lambda code=code : mode_button_click( code  ) ,fg_color="#032d3c" ,  bg_color="transparent")   
        tkinter_elements[element_name].grid(row=int(result["modes"][key]["row"]) , column=int(result["modes"][key]["column"]), padx=20, pady=(0, 20), sticky="w")


    color = customtkinter.CTkLabel(app, text="Color", font=('consola', 16, 'bold'))

    purple = customtkinter.CTkButton(app, text="Purple"  , command=lambda: color_button_click("Purple") , fg_color="#5999ff")

    yellow = customtkinter.CTkButton(app, text="Yellow" , fg_color="yellow" , bg_color="transparent" , text_color="black",    command=lambda: color_button_click("Yellow"))

    red = customtkinter.CTkButton(app, text="Red" , fg_color="#5999ff" , bg_color="transparent" , text_color="black",    command=lambda: color_button_click("Red"))

    box_size_text = customtkinter.CTkLabel(app, text="Box size", font=('consola', 16, 'bold'))

    box_size_sub_button =  customtkinter.CTkButton(app,  text="-" , font=('consola', 20)  , command=decrement_box_size)

    box_size_entry = customtkinter.CTkButton(app , state="normal" ,text="4" , fg_color="grey" , bg_color="transparent",   text_color="white" , font=('consola', 16))

    box_size_add_button =  customtkinter.CTkButton(app, text="+" , font=('consola', 20) , command=increment_box_size)


    custom_res_text = customtkinter.CTkLabel(app, text="resolution", font=('consola', 16, 'bold'))

    custom_w = customtkinter.CTkEntry(app, placeholder_text="Width")
    custom_h = customtkinter.CTkEntry(app, placeholder_text="Height")

    custom_res_button = customtkinter.CTkButton(app, text="use" , font=('consola', 14, 'bold'),command=use_custom_res)


    strafe_text = customtkinter.CTkLabel(app, text="shoot when moving", font=('consola', 16, 'bold'))



    def strafe_event():

        global strafeToggle
        global strafe_var

        strafeToggle = not strafeToggle
        
          
    strafe_var = customtkinter.StringVar(value="on")
    stafe_toggle = customtkinter.CTkSwitch(app, text="", command=strafe_event,
                                     variable=strafe_var, onvalue="on", offvalue="off", progress_color="#00FF00")
          


        

    toggle_text.grid(row=0, column=0, padx=(10,20), pady=20, sticky="w")
 
    switch.grid(row=0, column=1, padx=10, pady=20, sticky="w")
    wpn_text.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="w")
    color.grid(row=15, column=0, padx=(10,20), pady=(0, 20), sticky="w")
    purple.grid(row=16, column=0, padx=20, pady=(0, 20), sticky="w")
    yellow.grid(row=16, column=1, padx=20, pady=(0, 20), sticky="w")
    red.grid(row=16, column=2, padx=20, pady=(0, 20), sticky="w")

    box_size_text.grid(row=17, column=0,padx=(10 ,20), pady=(0, 20), sticky="w")
    box_size_sub_button.grid(row=18 , column=0 , padx=20, pady=(0, 20), sticky="w")
    box_size_entry.grid(row=18 , column=1 ,  padx=20, pady=(0, 20), sticky="w")
    box_size_add_button.grid(row=18 , column=2 , padx=20, pady=(0, 20), sticky="w")
    custom_res_text.grid(row=19, column=0, padx=(10 ,20), pady=(0, 20), sticky="w")
    custom_res_button.grid(row=20, column=2, padx=20, pady=(0, 20), sticky="w")
    custom_w.grid(row=20, column=0, padx=20, pady=(0, 20), sticky="w")
    custom_h.grid(row=20, column=1, padx=20, pady=(0, 20), sticky="w")

    strafe_text.grid(row=21, column=0, columnspan=2  ,padx=20, pady=(0, 20), sticky="w")
    stafe_toggle.grid(row=21, column=2, padx=20, pady=(0, 20), sticky="w")


    mode_button_click("vandal")
    app.mainloop()


# Optionally, you may want to join threads before exiting
for hotkey_thread in hotkey_threads:
    hotkey_thread.join()


