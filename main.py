from tkinter import Tk, PhotoImage, Canvas, Label, Entry, Button, END
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

DARK_BLUE = "#035397"
LIGHT_BLUE = "#035397"
FONT_NAME = "Courier"
BACKGROUND = "white"
LABEL_FONT = (FONT_NAME, 14, "bold")
BUTTON_FONT = (FONT_NAME, 12, "bold")


def clear():
    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def confirmation(username, password):
    message = f"These are the details information:\nUsername: {username}\nPassword: {password}\nThe information is correct?!"
    return messagebox.askyesno(title="website", message=message)


def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "username": username,
        "password": password,
    }}
    if len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showinfo(title="Oops", message="fill all the fields!")
    else:
        try:
            with open("data.json", "r") as data_file:
                json_data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                if confirmation(username, password):
                    json.dump(new_data, data_file, indent=4)
                else:
                    json.dump({}, data_file, indent=4)
        else:
            json_data.update(new_data)
            if confirmation(username, password):
                with open("data.json", "w") as data_file:
                    json.dump(json_data, data_file, indent=4)
        finally:
            clear()


def search():
    website = website_entry.get()
    if len(website) > 0:
        try:
            with open("data.json", "r") as data_file:
                json_data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(f"There is no information stored to {website}")
        else:
            if website in json_data:
                data = json_data.get(website)
                username = data["username"]
                password = data["password"]
                messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showinfo(f"There is no information stored to {website}")

# GUI
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BACKGROUND)

# Image
lock_image = PhotoImage(file="resources/images/lock_one.png")

# Canvas
canvas = Canvas(width=200, height=180, bg=BACKGROUND, highlightthickness=0)
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=1, column=1)

# Labels
website_label = Label(text="Website:", font=LABEL_FONT, bg=BACKGROUND)
website_label.grid(row=2, column=0)

username_label = Label(text="Email/Username:", font=LABEL_FONT, bg=BACKGROUND)
username_label.grid(row=3, column=0)

password_label = Label(text="Password:", font=LABEL_FONT, bg=BACKGROUND)
password_label.grid(row=4, column=0)

# Entries
website_entry = Entry()
website_entry.config(width=36)
website_entry.focus()
website_entry.grid(row=2, column=1, padx=5, pady=15)

username_entry = Entry()
username_entry.config(width=70)
username_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=15)

password_entry = Entry()
password_entry.config(width=36)
password_entry.grid(row=4, column=1, padx=5, pady=15)

# Buttons
search_button = Button(text="Search", width=18, font=BUTTON_FONT, padx=5, pady=1, command=search)
search_button.grid(row=2, column=2)

generate_password_button = Button(text="Generate Password", font=BUTTON_FONT, padx=5, pady=1, command=generate_password)
generate_password_button.grid(row=4, column=2)

add_button = Button(text="Add", font=BUTTON_FONT, width=42, command=save)
add_button.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

window.mainloop()
