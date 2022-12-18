from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
from pyperclip import copy
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    copy(password)
    password_entry.insert(END, password)
# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File not found", message="There is no data file")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \n Password: {password}")
        else:
            messagebox.showerror(title="Website not found", message=f"Website {website} not found")
# ---------------------------- SAVE PASSWORD ------------------------------- #

def add():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email" : email,
            "password" : password,
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showerror(title="Error", message="Please don't leave any entry empty!")
    else:
        is_okay = messagebox.askokcancel(title="Check your inputs", message=f"These are the details entered: \nWebsite: {website}"
                                                         f"\nEmail: {email}"
                                                         f"\nPassword: {password}"
                                                         f"\nIs it okay to save?")
        if is_okay:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)
website_text = Label(text="Website:")
website_text.grid(row=1, column=0)
email_text = Label(text="Email/Username:")
email_text.grid(row=2, column=0)
password_text = Label(text="Password:")
password_text.grid(row=3,column=0)
website_entry = Entry(width=18)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2,column=1, columnspan=2)
email_entry.insert(END, "some_email@gmail.com")
password_entry = Entry(width=18)
password_entry.grid(row=3,column=1)
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=add)
add_button.grid(row=4,column=1,columnspan=2)
search_button = Button(text="Search", command=search, width=13)
search_button.grid(row=1,column=2)


window.mainloop()