from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from cryptography.fernet import Fernet

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Function
def generate_password():
    small_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']
    capital_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z',]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_small_letters = [choice(small_letters) for _ in range(randint(8, 10))]
    password_capital_letters = [choice(capital_letters) for _ in range(randint(4, 8))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_small_letters + password_capital_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get()
    email = email_entry.get()
    my_key = Fernet.generate_key().decode()
    password = password_entry.get()
    password_key = my_encrypt(my_key, data=password).decode()
    new_data = {
        website: {
            "email": email,
            "password_key": password_key,
            "key": my_key,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- DELETE PASSWORD ------------------------------- #
def delete():
    website = website_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password_key": "",
            "key": "",
        }
    }
    if len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please fill in your email.")
    elif len(website) == 0:
        messagebox.showinfo(title="Oopsie", message="First fill in the website you want to delete password of")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Deleting updated data
                json.dump(data, data_file, indent=4)
        except:
            messagebox.showinfo(title="Oops", message="No password has been saved for the given details")
        else:
            messagebox.showinfo(title="Password", message=f"For {website} and {email} your password has been deleted")
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- Encrypter And Decrypter ------------------------------- #

# Encrypter Function

def my_encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Decrypter Function
def my_decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data).decode()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    email = email_entry.get()
    if len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please fill in your email.")
    elif len(website) == 0:
        messagebox.showinfo(title="Oopsie", message="Try filling in website you were searching for.")
    else:
        try:
            print(1)
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
            if website in data:
                pass
            else:
                messagebox.showinfo(title="Password Unavailable", message="There is no password saved for the given "
                                                                          "details.")
                return
            print(2)
        except:
            messagebox.showinfo(title="Oops", message="First you should "
                                                      "try to save some passwords before searching for one.")
        else:
            key = data[website]["key"].encode()
            encrypted_password = data[website]["password_key"]
            password = my_decrypt(key=key, data=encrypted_password)
            messagebox.showinfo(title="Password", message=f"For {website} and {email} "
                                                          f"your password is:\n{password}")
            pyperclip.copy(password)
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            # for i in data[website]:
            #     if data[website][] == email:
            #         messagebox.showinfo(title="YOUR PASSWORD", message=f"Your password for \n"
            #                                                            f"{website} and {email}:\n"
            #                                                            f"{data[website]['password']}.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=38)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=56)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "@gmail.com")
password_entry = Entry(width=38)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=48, command=save)
add_button.grid(row=4, column=1, columnspan=2)
delete_button = Button(text='Delete', width=10,command=delete)
delete_button.grid(row=4, column=0)

window.mainloop()
