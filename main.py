# Lock image found in Font Awesome
# tkinter by John Ousterhout
# Pillow made by Alex Clark and Contributors

import random
from tkinter import *
from PIL import ImageTk, Image

lettr_char = ""
speci_char = ""
numbr_char = ""

passwords = [] # important at

# -------- Setting up characters and functions --

# getting both upper and lower case letter
for i in range(65, 123):
    if not (i >= 91 and i <= 96):
        lettr_char += str(chr(i))

for i in range (33, 127):
    # getting all special characters
    if (i >= 33 and i <= 47) or (i >= 58 and i <= 64) or (i >= 91 and i <= 96) or (i >= 123 and i <= 126):
        if i == 34:
            speci_char += f"\{str(chr(i))}"
        else:
            speci_char += str(chr(i))

    # getting all numbers
    elif (i >= 48 and i <= 57):
        numbr_char += str(chr(i))

# to generate the password, checking if the user want special characters and/or numbers
def generate_pass(length: int, special_char: bool, number_char: bool):
    new_password = ""

    for i in range(length):
        if special_char == True and number_char == True:
            char = lettr_char+speci_char+numbr_char
            new_password = char[random.randrange(0, len(char))] + new_password

        elif special_char == True and number_char == False:
            char = lettr_char+speci_char
            new_password = char[random.randrange(0, len(char))] + new_password

        elif special_char == False and number_char == True:
            char = lettr_char+numbr_char
            new_password = char[random.randrange(0, len(char))] + new_password

        else:
            new_password = lettr_char[random.randrange(0, len(lettr_char))] + new_password

    return new_password

# -------- The main application --
window = Tk()
window.title("PASSgen")
window.geometry("300x375")

# LOGO IMG and COPYRIGHT
logoImg = Image.open("logo.png")
resizedLogo = logoImg.resize((202,70), Image.ANTIALIAS) # resizing image
new_pic = ImageTk.PhotoImage(resizedLogo)
Label(window, image=new_pic).pack(side=TOP)

# MAIN PASS OPTIONS
Label(window, text="Name of the Password", justify=RIGHT).pack(side=TOP, fill=BOTH, expand=True)
e1 = Entry(window)
e1.pack()

Label(window, text="Length of Password", justify=RIGHT).pack(side=TOP, fill=BOTH, expand=True)
e2 = Entry(window)
e2.pack()

v1 = IntVar()
v2 = IntVar()
Checkbutton(window, text="Add Special Characters? (e,g; $,%,&)", variable=v1).pack(side=TOP, fill=BOTH, expand=True)
Checkbutton(window, text="Add Numbers?", variable=v2).pack(side=TOP, fill=BOTH, expand=True)

# ALL DEF PARAM FOR BTN'S
def get_pass():
    # TODO: Do the same with the name, but make it so it can detect str. Same with length with int.

    namepw = e1.get()
    length = int(e2.get())
    specia = False
    number = False
    if v1.get() == 1:
        specia = True
    if v2.get() == 1:
        number = True

    found = False
    for i in passwords:
        for j in i:
            if j.lower() == namepw.lower():
                found = True
                break
            else:
                continue

    if found == True:
        info.config(text=f"\n\"{namepw}\" is already generated...\n", fg="red")
    else:
        if length > 16 or length < 5:
            info.config(text="\nLength must be between 5 and 16.\n", fg="red")
        else:
            password_window = Toplevel(window)
            password_window.title("Generated Password")

            created_pass = generate_pass(length, specia, number)

            passwords.append([namepw, created_pass])

            Label(password_window, text=f"Password for {namepw}:\n{created_pass}\n").pack(side=TOP, fill=BOTH, pady=10)
            info.config(text="\nConfirm Generated Password\n", fg="black")

            def add_more_pass():
                info.config(text="\nYou can add one more password...\n", fg="red")
                password_window.destroy()
            def no():
                password_window.destroy()
                info.config(text="\nClick on 'Show Stored Passwords' to see\npasswords and you may close the window.\n", fg="red")
                gen_btn.config(state=DISABLED)

            Label(password_window, text=f"Add another password?").pack(side=TOP, fill=BOTH)
            Button(password_window, text="Yes", command=add_more_pass).pack(side=TOP, pady=(0,10))

            Button(password_window, text="No", fg="red", command=no).pack(side=TOP, pady=(0,10))

import os
from sys import platform

def show_all():
    # TODO: With the checkbox, make it so it can delete certain passwords
    # TODO: Add a save button, where the user can save the password in a .txt file
    listed_pass = Toplevel(window)
    listed_pass.title("Listed Passwords")
    frame = Frame(listed_pass)
    frame.pack()

    title1 = Label(frame, text="Name", padx=5, pady=5, width=16)
    title1.grid(row=0, column=0)

    title2 = Label(frame, text="Password", padx=5, pady=5, width=16)
    title2.grid(row=0, column=1)

    j = 1
    for i in passwords:

        name = Label(frame, text=i[0], padx=5, pady=5, width=16)
        name.grid(row=j, column=0)

        genpass = Label(frame, text=i[1], padx=5, pady=5, width=16)
        genpass.grid(row=j, column=1)

        select = Checkbutton(frame)
        select.grid(row=j, column=2)

        j += 1

    def delete_pass():
        print("Deleting Password(s)....")

    def save_pass():
        try:
            with open("saved_passwords.txt", "w") as f:
                for i in passwords:
                    f.write(f"{i[0]}: {i[1]}\n")
                f.write("\nDon't forget to copy the text here!")
        except:
            l_info.config(text="There has been an error...", fg="red")
        else:
            l_info.config(text="Password is saved!", fg="black")

    l_info = Label(frame, text="\n")
    l_info.grid(row=j, column=0, columnspan=1)

    Button(frame, text="Save Passwords", padx=5, pady=5, width=15, command=save_pass).grid(row=j+1, column=0)
    Button(frame, text="Delete", padx=5, pady=5, width=15, command=delete_pass).grid(row=j+1, column=1)

# GETTING INFO ON WHAT IS HAPPENING
info = Label(window, text="\nFill out the info above...\n", justify=CENTER)
info.pack(side=TOP, fill=BOTH, expand=True)

# BUTTONS
gen_btn = Button(window, text="Generate Password", command=get_pass)
gen_btn.pack(side=TOP, pady=(0,10))

stored_btn = Button(window, text="Show Stored Passwords", command=show_all)
stored_btn.pack(side=BOTTOM, pady=(0,10))

# TO OPEN THE WINDOW
window.mainloop()
