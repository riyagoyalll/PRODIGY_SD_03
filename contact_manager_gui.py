import tkinter as tk
from tkinter import messagebox
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")

        self.contacts = load_contacts()

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.setup_gui()
        self.display_contacts()

    def setup_gui(self):
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.phone_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.email_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add / Update", command=self.add_contact).grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Delete", command=self.delete_contact).grid(row=3, column=1, pady=10)

        self.contacts_listbox = tk.Listbox(self.root, width=50)
        self.contacts_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_select)

    def display_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.contacts_listbox.insert(tk.END, f"{name} | {details['phone']} | {details['email']}")

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name or not phone or not email:
            messagebox.showwarning("Missing Info", "All fields are required!")
            return

        self.contacts[name] = {"phone": phone, "email": email}
        save_contacts(self.contacts)
        self.display_contacts()
        self.clear_fields()
        messagebox.showinfo("Success", f"Contact for '{name}' saved!")

    def delete_contact(self):
        name = self.name_var.get().strip()
        if name in self.contacts:
            del self.contacts[name]
            save_contacts(self.contacts)
            self.display_contacts()
            self.clear_fields()
            messagebox.showinfo("Deleted", f"Contact for '{name}' deleted.")
        else:
            messagebox.showerror("Error", f"Contact for '{name}' does not exist.")

    def on_select(self, event):
        if not self.contacts_listbox.curselection():
            return
        index = self.contacts_listbox.curselection()[0]
        selected_line = self.contacts_listbox.get(index)
        name, phone, email = selected_line.split(" | ")
        self.name_var.set(name)
        self.phone_var.set(phone)
        self.email_var.set(email)

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()