import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import matplotlib.pyplot as plt
import pyttsx3
import speech_recognition as sr
import re
from tkcalendar import Calendar
import numpy as np
=======
=======
>>>>>>> Stashed changes
import pyttsx3

>>>>>>> Stashed changes
import json
import os
import pandas as pd
from fpdf import FPDF

<<<<<<< Updated upstream
<<<<<<< Updated upstream
from database import create_table, register_user, validate_user, add_transactions as db_add_transaction, get_transactions,get_transaction_by_id, update_transaction, delete_transaction

CONFIG_FILE = "user_config.json"
=======
=======
>>>>>>> Stashed changes
from database import create_table, register_user, validate_user, add_transactions as db_add_transaction, get_transactions

CONFIG_FILE = "user_config.json"

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
DATA_FILE = "transactions.json"
REMEMBER_FILE = "remember_user.json"

# Global variables
chat_box = None
current_user = None
transactions = []
main_window = None
trans_type = None
amount_entry = None
category_entry = None
chart_selector = None
transaction_tree = None

<<<<<<< Updated upstream
<<<<<<< Updated upstream
income_var = None
expense_var = None
balance_var = None

=======
def hash_password(password):
    import hashlib
    return hashlib.sha26(password.encode()).hexdigest()

=======
def hash_password(password):
    import hashlib
    return hashlib.sha26(password.encode()).hexdigest()

>>>>>>> Stashed changes
import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import json
import os
from PIL import Image, ImageTk

REMEMBER_FILE = "remember_user.json"

def show_login():
    login_win = tk.Tk()
    login_win.title("Login - Voice Enabled Personal Finance Tracker")
    login_win.geometry("400x450")

    current_theme = {"bg": "#002B36", "fg": "white"}
    login_win.configure(bg=current_theme["bg"])

    def speak_welcome():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say("Welcome back to your Finance Assistant.")
        engine.runAndWait()
    speak_welcome()

    try:
        img = Image.open("logo1.png").resize((80, 80))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(login_win, image=logo, bg=current_theme["bg"])
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        pass

    title_label = tk.Label(login_win, text="", font=("Helvetica", 16, "bold"), bg=current_theme["bg"], fg=current_theme["fg"])
    title_label.pack(pady=5)

    def animate_title(index=0):
        text = "Login to Finance Assistant"
        if index <= len(text):
            title_label.config(text=text[:index])
            login_win.after(80, animate_title, index + 1)
    animate_title()

    tk.Label(login_win, text="Voice-enabled personal finance tracker", font=("Helvetica", 10), bg=current_theme["bg"], fg="#AAAAAA").pack(pady=2)

    tk.Label(login_win, text="Username", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(20, 5))
    username_entry = ttk.Entry(login_win, font=("Segoe UI", 10))
    username_entry.pack(pady=5, ipady=3)

    tk.Label(login_win, text="Password", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    password_entry = ttk.Entry(login_win, show="*", font=("Segoe UI", 10))
    password_entry.pack(pady=5, ipady=3)

    remember_var = tk.BooleanVar()
    tk.Checkbutton(login_win, text="Remember Me", variable=remember_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme["bg"]).pack(pady=(10, 0))

    if os.path.exists(REMEMBER_FILE):
        with open(REMEMBER_FILE, "r") as f:
            data = json.load(f)
            username_entry.insert(0, data.get("username", ""))
            remember_var.set(True)

    def attempt_login():
        from database import validate_user
        username = username_entry.get()
        password = password_entry.get()
        if validate_user(username, password):
            if remember_var.get():
                with open(REMEMBER_FILE, "w") as f:
                    json.dump({"username": username}, f)
            elif os.path.exists(REMEMBER_FILE):
                os.remove(REMEMBER_FILE)
            messagebox.showinfo("Success", "Login successful!")
            login_win.destroy()
            show_splash(username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_win, text="Login", command=attempt_login, bg="#00C853", fg="white", activebackground="#00A843", font=("Segoe UI", 10, "bold"), padx=10, pady=5, relief="flat").pack(pady=20)

    def toggle_theme():
        if current_theme["bg"] == "#002B36":
            current_theme.update({"bg": "#f0f0f0", "fg": "black"})
        else:
            current_theme.update({"bg": "#002B36", "fg": "white"})

        login_win.configure(bg=current_theme["bg"])
        for widget in login_win.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton)):
                widget.config(bg=current_theme["bg"], fg=current_theme["fg"])

    tk.Button(login_win, text="Toggle Theme", command=toggle_theme, bg="#455A64", fg="white", font=("Segoe UI", 9), relief="flat").pack(pady=5)

    login_win.mainloop()

    
def add_transactions():
    type_ = trans_type.get()
    amount = amount_entry.get()
    category = category_entry.get()

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return

    db_add_transaction(type_, amount, category)
    load_data()    

    update_summary()  # Then update summary
    show_chart(chart_selector.get())  # And refresh chart
    messagebox.showinfo("Success", f"{type_} added successfully!")
    
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
# Update summary
>>>>>>> Stashed changes
def update_summary():
    if not income_var or not expense_var or not balance_var:
        return
        
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    balance = income - expense

    income_var.set(f"₹ {income:.2f}")
    expense_var.set(f"₹ {expense:.2f}")
    balance_var.set(f"₹ {balance:.2f}")

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def update_chat(msg, sender="You"):
    global chat_box
    if chat_box:
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"{sender}: {msg}\n")
        chat_box.see(tk.END)
        chat_box.config(state="disabled")

def toggle_password_visibility(entry, toggle_btn):
    if entry.cget('show') == '':
        entry.config(show='*')
        toggle_btn.config(text='👁️‍🗨️')
    else:
        entry.config(show='')
        toggle_btn.config(text='🙈')

def show_login():
    login_win = tk.Tk()
    login_win.title("Login - Voice Enabled Personal Finance Tracker")
    login_win.geometry("400x450")

    current_theme = {"bg": "#002B36", "fg": "white"}
    login_win.configure(bg=current_theme["bg"])

    def speak_welcome():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say("Welcome back to your Finance Assistant.")
            engine.runAndWait()
        except:
            pass  

    speak_welcome()

    # Logo 
    try:
        img = Image.open("logo1.png").resize((80, 80))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(login_win, image=logo, bg=current_theme["bg"])
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        logo_label = tk.Label(login_win, text="💰", font=("Arial", 40), bg=current_theme["bg"], fg=current_theme["fg"])
        logo_label.pack(pady=10)

    title_label = tk.Label(login_win, text="", font=("Helvetica", 16, "bold"), bg=current_theme["bg"], fg=current_theme["fg"])
    title_label.pack(pady=5)

    def animate_title(index=0):
        text = "Login to Finance Assistant"
        if index <= len(text):
            title_label.config(text=text[:index])
            login_win.after(80, animate_title, index + 1)
    
<<<<<<< Updated upstream
    animate_title()

    tk.Label(login_win, text="Voice-enabled personal finance tracker", font=("Helvetica", 10), bg=current_theme["bg"], fg="#AAAAAA").pack(pady=2)

    tk.Label(login_win, text="Username", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(20, 5))
    username_entry = ttk.Entry(login_win, font=("Segoe UI", 10))
    username_entry.pack(pady=5, ipady=3)
    username_entry.focus()

    tk.Label(login_win, text="Password", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    password_entry = ttk.Entry(login_win, show="*", font=("Segoe UI", 10))
    password_entry.pack(pady=5, ipady=3)

    remember_var = tk.BooleanVar()
    tk.Checkbutton(login_win, text="Remember Me", variable=remember_var, bg=current_theme["bg"], fg=current_theme["fg"], selectcolor=current_theme["bg"]).pack(pady=(10, 0))

    # Remember user if exists
    if os.path.exists(REMEMBER_FILE):
        try:
            with open(REMEMBER_FILE, "r") as f:
                data = json.load(f)
                username_entry.insert(0, data.get("username", ""))
                remember_var.set(True)
        except:
            pass

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
            
        if validate_user(username, password):
            global current_user
            current_user = username
            
            if remember_var.get():
                try:
                    with open(REMEMBER_FILE, "w") as f:
                        json.dump({"username": username}, f)
                except:
                    pass
            elif os.path.exists(REMEMBER_FILE):
                try:
                    os.remove(REMEMBER_FILE)
                except:
                    pass

            messagebox.showinfo("Success", "Login successful!")
            login_win.destroy()
            show_splash(username)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_win, text="Login", command=attempt_login, bg="#00C853", fg="white", activebackground="#00A843", font=("Segoe UI", 10, "bold"), padx=10, pady=5, relief="flat").pack(pady=20)
    
    # Register button
    tk.Button(login_win, text="Register New Account", command=lambda: [login_win.destroy(), show_register_window()], bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5, relief="flat").pack(pady=5)

    login_win.bind('<Return>', lambda event: attempt_login())

    def toggle_theme():
        if current_theme["bg"] == "#002B36":
            current_theme.update({"bg": "#f0f0f0", "fg": "black"})
        else:
            current_theme.update({"bg": "#002B36", "fg": "white"})

        login_win.configure(bg=current_theme["bg"])
        for widget in login_win.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton)):
                try:
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
                except:
                    pass

    tk.Button(login_win, text="Toggle Theme", command=toggle_theme, bg="#455A64", fg="white", font=("Segoe UI", 9), relief="flat").pack(pady=5)

    login_win.mainloop()

def show_register_window():
    reg_win = tk.Tk()
    reg_win.title("Register - Personal Finance Tracker")
    reg_win.geometry("400x450")
    
    current_theme = {"bg": "#002B36", "fg": "white"}
    reg_win.configure(bg=current_theme["bg"])

    # Logo
    try:
        img = Image.open("logo1.png").resize((80, 80))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(reg_win, image=logo, bg=current_theme["bg"])
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        logo_label = tk.Label(reg_win, text="💰", font=("Arial", 40), bg=current_theme["bg"], fg=current_theme["fg"])
        logo_label.pack(pady=10)

    title_label = tk.Label(reg_win, text="", font=("Helvetica", 16, "bold"), bg=current_theme["bg"], fg=current_theme["fg"])
    title_label.pack(pady=5)

    def animate_title(index=0):
        full_text = "Create Your Finance Account"
        if index <= len(full_text):
            title_label.config(text=full_text[:index])
            reg_win.after(80, animate_title, index + 1)

    animate_title()

    tk.Label(reg_win, text="Voice-enabled personal finance tracker", font=("Helvetica", 10), bg=current_theme["bg"], fg="#AAAAAA").pack(pady=2)

    tk.Label(reg_win, text="Username", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(20, 5))
    username_entry = ttk.Entry(reg_win, font=("Segoe UI", 10))
    username_entry.pack(pady=5, ipady=3)
    username_entry.focus()

    tk.Label(reg_win, text="Password", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    password_entry = ttk.Entry(reg_win, show="*", font=("Segoe UI", 10))
    password_entry.pack(pady=5, ipady=3)

    def register_now():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
            
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long.")
            return
            
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters long.")
            return
            
        if register_user(username, password):
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            reg_win.destroy()
            with open(CONFIG_FILE, "w") as f:
                json.dump({"registered": True}, f)
            show_login()
        else:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")

    reg_btn = tk.Button(reg_win, text="Register", command=register_now, bg="#00C853", fg="white", activebackground="#00A843", font=("Segoe UI", 10, "bold"), padx=10, pady=5, relief="flat")
    reg_btn.pack(pady=20)
    
    # Back to login "Button"
    tk.Button(reg_win, text="Back to Login", command=lambda: [reg_win.destroy(), show_login()], bg="#757575", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5, relief="flat").pack(pady=5)

    def toggle_theme():
        if current_theme["bg"] == "#002B36":
            current_theme.update({"bg": "#f0f0f0", "fg": "black"})
        else:
            current_theme.update({"bg": "#002B36", "fg": "white"})

        reg_win.configure(bg=current_theme["bg"])
        for widget in reg_win.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton)):
                try:
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
                except:
                    pass

    theme_btn = tk.Button(reg_win, text="Toggle Theme", command=toggle_theme, bg="#455A64", fg="white", font=("Segoe UI", 9), relief="flat")
    theme_btn.pack(pady=5)

    reg_win.mainloop()

def add_transactions():
    if not trans_type or not amount_entry or not category_entry:
        messagebox.showerror("Error", "Form elements not initialized!")
        return
        
    type_ = trans_type.get()
    amount_str = amount_entry.get()
    category = category_entry.get()
    
    if not amount_str or not category:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    try:
        amount = float(amount_str)
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0!")
            return
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!")
        return

    note = "Manual Transaction"
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        db_add_transaction(current_user, type_, amount, category, note, date)
        load_data()
        update_summary()
        refresh_transaction_list()
        
        # Update chart 
        if chart_selector:
            show_chart(chart_selector.get())
            
        messagebox.showinfo("Success", f"{type_} of ₹{amount} added successfully!")

        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add transaction: {str(e)}")

def refresh_transaction_list():
    global transaction_tree
    if transaction_tree:
        # To Clear existing items
        for item in transaction_tree.get_children():
            transaction_tree.delete(item)
        
        # Inserting of updated transactions
        for transaction in transactions:
            transaction_tree.insert('', 'end', values=(
                transaction['id'],
                transaction['type'],
                f"₹{transaction['amount']:.2f}",
                transaction['category'],
                transaction['note'],
                transaction['date']
            ))

def show_transaction_manager():
    global transaction_tree
    
    manager_win = tk.Toplevel(main_window)
    manager_win.title("Transaction Manager - View, Edit & Delete")
    manager_win.geometry("900x600")
    manager_win.configure(bg="#f5f5f5")
    
    # Title
    title_label = tk.Label(manager_win, text="📋 Transaction Manager", 
                          font=("Segoe UI", 18, "bold"), bg="#f5f5f5", fg="#333")
    title_label.pack(pady=10)
    
    # To filter transactions
    search_frame = tk.Frame(manager_win, bg="#f5f5f5")
    search_frame.pack(fill="x", padx=20, pady=5)
    
    tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").pack(side="left", padx=5)
    
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side="left", padx=5)
    
    def search_transactions():
        search_term = search_var.get().lower()
        
        for item in transaction_tree.get_children():
            transaction_tree.delete(item)
        
        for transaction in transactions:
            if (search_term in transaction['category'].lower() or 
                search_term in transaction['type'].lower() or
                search_term in transaction['note'].lower() or
                search_term in str(transaction['amount'])):
                
                transaction_tree.insert('', 'end', values=(
                    transaction['id'],
                    transaction['type'],
                    f"₹{transaction['amount']:.2f}",
                    transaction['category'],
                    transaction['note'],
                    transaction['date']
                ))
    
    tk.Button(search_frame, text="Search", command=search_transactions, 
              bg="#2196F3", fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
    
    tk.Button(search_frame, text="Clear", 
              command=lambda: [search_var.set(""), refresh_transaction_list()], 
              bg="#757575", fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
    
    list_frame = tk.Frame(manager_win, bg="#f5f5f5")
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    columns = ('ID', 'Type', 'Amount', 'Category', 'Note', 'Date')
    transaction_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    # headings
    transaction_tree.heading('ID', text='ID')
    transaction_tree.heading('Type', text='Type')
    transaction_tree.heading('Amount', text='Amount')
    transaction_tree.heading('Category', text='Category')
    transaction_tree.heading('Note', text='Note')
    transaction_tree.heading('Date', text='Date')
    
    # column width
    transaction_tree.column('ID', width=50)
    transaction_tree.column('Type', width=80)
    transaction_tree.column('Amount', width=100)
    transaction_tree.column('Category', width=120)
    transaction_tree.column('Note', width=200)
    transaction_tree.column('Date', width=100)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=transaction_tree.yview)
    transaction_tree.configure(yscrollcommand=scrollbar.set)
    
    transaction_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Button frame
    button_frame = tk.Frame(manager_win, bg="#f5f5f5")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    def edit_selected_transaction():
        selection = transaction_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a transaction to edit.")
            return
        
        item = transaction_tree.item(selection[0])
        transaction_id = item['values'][0]
        show_edit_transaction_dialog(transaction_id)
    
    def delete_selected_transaction():
        selection = transaction_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return
        
        item = transaction_tree.item(selection[0])
        transaction_id = item['values'][0]
        transaction_type = item['values'][1]
        amount = item['values'][2]
        category = item['values'][3]
        
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete this transaction?\n\n"
                                   f"Type: {transaction_type}\n"
                                   f"Amount: {amount}\n"
                                   f"Category: {category}")
        
        if result:
            try:
                delete_transaction(transaction_id)
                load_data()
                update_summary()
                refresh_transaction_list()
                messagebox.showinfo("Success", "Transaction deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")
    
    def view_selected_transaction():
        selection = transaction_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a transaction to view.")
            return
        
        item = transaction_tree.item(selection[0])
        values = item['values']
        
        details = f"""
Transaction Details:

ID: {values[0]}
Type: {values[1]}
Amount: {values[2]}
Category: {values[3]}
Note: {values[4]}
Date: {values[5]}
        """
        
        messagebox.showinfo("Transaction Details", details)
    
    # Buttons
    tk.Button(button_frame, text="👁️ View Details", command=view_selected_transaction, 
              bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="✏️ Edit Transaction", command=edit_selected_transaction, 
              bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🗑️ Delete Transaction", command=delete_selected_transaction, 
              bg="#F44336", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 Refresh List", command=refresh_transaction_list, 
              bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ Close", command=manager_win.destroy, 
              bg="#757575", fg="white", font=("Segoe UI", 10, "bold")).pack(side="right", padx=5)
    
    refresh_transaction_list()

def show_edit_transaction_dialog(transaction_id):
    transaction = None
    for t in transactions:
        if t['id'] == transaction_id:
            transaction = t
            break
    
    if not transaction:
        messagebox.showerror("Error", "Transaction not found!")
        return
    
    edit_win = tk.Toplevel(main_window)
    edit_win.title("Edit Transaction")
    edit_win.geometry("400x500")
    edit_win.configure(bg="#f5f5f5")
    edit_win.grab_set()  
    
    # Title
    tk.Label(edit_win, text="✏️ Edit Transaction", font=("Segoe UI", 16, "bold"), 
             bg="#f5f5f5", fg="#333").pack(pady=20)
    
    # Form frame
    form_frame = tk.Frame(edit_win, bg="#f5f5f5")
    form_frame.pack(pady=20, padx=40, fill="both", expand=True)
    
    # Transaction ID (read-only)
    tk.Label(form_frame, text="Transaction ID:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=0, column=0, sticky="w", pady=5)
    tk.Label(form_frame, text=str(transaction_id), font=("Segoe UI", 10), 
             bg="#f5f5f5", fg="#666").grid(row=0, column=1, sticky="w", padx=10, pady=5)
    
    # Type
    tk.Label(form_frame, text="Type:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=1, column=0, sticky="w", pady=5)
    type_var = tk.StringVar(value=transaction['type'])
    type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                             values=["Income", "Expense"], state="readonly", width=20)
    type_combo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
    
    # Amount
    tk.Label(form_frame, text="Amount (₹):", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=2, column=0, sticky="w", pady=5)
    amount_var = tk.StringVar(value=str(transaction['amount']))
    amount_entry = ttk.Entry(form_frame, textvariable=amount_var, width=20)
    amount_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
    
    # Category
    tk.Label(form_frame, text="Category:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=3, column=0, sticky="w", pady=5)
    category_var = tk.StringVar(value=transaction['category'])
    category_entry = ttk.Entry(form_frame, textvariable=category_var, width=20)
    category_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
    
    # Note
    tk.Label(form_frame, text="Note:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=4, column=0, sticky="w", pady=5)
    note_var = tk.StringVar(value=transaction['note'])
    note_entry = ttk.Entry(form_frame, textvariable=note_var, width=20)
    note_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
    
    # Date
    tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=5, column=0, sticky="w", pady=5)
    date_var = tk.StringVar(value=transaction['date'])
    date_entry = ttk.Entry(form_frame, textvariable=date_var, width=20)
    date_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
    
    # update function
    def update_transaction_data():
        try:
            new_type = type_var.get()
            new_amount = float(amount_var.get())
            new_category = category_var.get().strip()
            new_note = note_var.get().strip()
            new_date = date_var.get().strip()
            
            if not new_category:
                messagebox.showerror("Error", "Category cannot be empty!")
                return
            
            if new_amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0!")
                return
            
            # Valid Date
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
            
            update_transaction(transaction_id, new_type, new_amount, new_category, new_note, new_date)
            
            load_data()
            update_summary()
            refresh_transaction_list()
            
            messagebox.showinfo("Success", "Transaction updated successfully!")
            edit_win.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update transaction: {str(e)}")
    
    # Button frame
    button_frame = tk.Frame(edit_win, bg="#f5f5f5")
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="💾 Save Changes", command=update_transaction_data, 
              bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), padx=20).pack(side="left", padx=10)
    
    tk.Button(button_frame, text="❌ Cancel", command=edit_win.destroy, 
              bg="#757575", fg="white", font=("Segoe UI", 11, "bold"), padx=20).pack(side="left", padx=10)
    
    amount_entry.focus()

def delete_transaction_by_id(transaction_id):
    try:
        delete_transaction(transaction_id)
        
        load_data()
        update_summary()
        
        # To Refresh UI 
        if 'transaction_tree' in globals() and transaction_tree:
            refresh_transaction_list()
        
        if chart_selector:
            show_chart(chart_selector.get())
            
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete transaction: {str(e)}")
        return False

def get_transaction_details(transaction_id):
    try:
        transaction_data = get_transaction_by_id(transaction_id)
        
        if transaction_data:
            return {
                'id': transaction_data[0],
                'type': transaction_data[1],
                'amount': transaction_data[2],
                'category': transaction_data[3],
                'note': transaction_data[4],
                'date': transaction_data[5]
            }
        else:
            return None
    except Exception as e:
        print(f"Error getting transaction details: {e}")
        return None

def show_transaction_details_popup(transaction_id):
    transaction = get_transaction_details(transaction_id)
    
    if not transaction:
        messagebox.showerror("Error", "Transaction not found!")
        return
    
    details = f"""
📋 Transaction Details

ID: {transaction['id']}
Type: {transaction['type']}
Amount: ₹{transaction['amount']:.2f}
Category: {transaction['category']}
Note: {transaction['note']}
Date: {transaction['date']}
    """
    
    messagebox.showinfo("Transaction Details", details)

def create_new_transaction_dialog():
    create_win = tk.Toplevel(main_window)
    create_win.title("Add New Transaction")
    create_win.geometry("400x450")
    create_win.configure(bg="#f5f5f5")
    create_win.grab_set()
    
    # Title
    tk.Label(create_win, text="➕ Add New Transaction", font=("Segoe UI", 16, "bold"), 
             bg="#f5f5f5", fg="#333").pack(pady=20)
    
    # Form frame
    form_frame = tk.Frame(create_win, bg="#f5f5f5")
    form_frame.pack(pady=20, padx=40, fill="both", expand=True)
    
    # Type
    tk.Label(form_frame, text="Type:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=0, column=0, sticky="w", pady=5)
    type_var = tk.StringVar(value="Income")
    type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                             values=["Income", "Expense"], state="readonly", width=20)
    type_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
    
    # Amount
    tk.Label(form_frame, text="Amount (₹):", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=1, column=0, sticky="w", pady=5)
    amount_var = tk.StringVar()
    amount_entry = ttk.Entry(form_frame, textvariable=amount_var, width=20)
    amount_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
    
    # Category
    tk.Label(form_frame, text="Category:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=2, column=0, sticky="w", pady=5)
    category_var = tk.StringVar()
    category_entry = ttk.Entry(form_frame, textvariable=category_var, width=20)
    category_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
    
    # Note
    tk.Label(form_frame, text="Note:", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=3, column=0, sticky="w", pady=5)
    note_var = tk.StringVar(value="Manual Transaction")
    note_entry = ttk.Entry(form_frame, textvariable=note_var, width=20)
    note_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
    
    # Date
    tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 10, "bold"), 
             bg="#f5f5f5").grid(row=4, column=0, sticky="w", pady=5)
    date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    date_entry = ttk.Entry(form_frame, textvariable=date_var, width=20)
    date_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
    

def filter_transactions_by_date_range(start_date, end_date):
    try:
        filtered_transactions = []
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d")
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start <= transaction_date <= end:
                filtered_transactions.append(transaction)
        
        return filtered_transactions
    except Exception as e:
        print(f"Error filtering transactions: {e}")
        return []

def filter_transactions_by_type(transaction_type):
    return [t for t in transactions if t['type'] == transaction_type]

def filter_transactions_by_category(category):
    return [t for t in transactions if t['category'].lower() == category.lower()]

def get_transaction_summary():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    balance = total_income - total_expense
    
    income_categories = {}
    expense_categories = {}
    
    for transaction in transactions:
        category = transaction['category']
        amount = transaction['amount']
        
        if transaction['type'] == 'Income':
            income_categories[category] = income_categories.get(category, 0) + amount
        else:
            expense_categories[category] = expense_categories.get(category, 0) + amount
    
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transaction_count': len(transactions),
        'income_categories': income_categories,
        'expense_categories': expense_categories
    }

def add_crud_buttons_to_main_window(parent_frame):
    crud_frame = tk.LabelFrame(parent_frame, text="Transaction Management 📋", 
                              font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=15, pady=15)
    crud_frame.pack(fill="x", padx=5, pady=5)
    
    # CRUD Buttons
    button_frame = tk.Frame(crud_frame, bg="#ECEFF1")
    button_frame.pack(fill="x", pady=5)

    
    tk.Button(button_frame, text="📋 Manage Transactions", command=show_transaction_manager,
              bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    def show_summary():
        summary = get_transaction_summary()
        summary_text = f"""
📊 Transaction Summary

Total Income: ₹{summary['total_income']:.2f}
Total Expense: ₹{summary['total_expense']:.2f}
Balance: ₹{summary['balance']:.2f}
Total Transactions: {summary['transaction_count']}

Top Income Categories:
{chr(10).join([f"• {cat}: ₹{amt:.2f}" for cat, amt in sorted(summary['income_categories'].items(), key=lambda x: x[1], reverse=True)[:3]])}

Top Expense Categories:
{chr(10).join([f"• {cat}: ₹{amt:.2f}" for cat, amt in sorted(summary['expense_categories'].items(), key=lambda x: x[1], reverse=True)[:3]])}
        """
        messagebox.showinfo("Transaction Summary", summary_text)
    
    tk.Button(button_frame, text="📈 Show Summary", command=show_summary,
              bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        
        

def show_budget_suggestion():
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    
    suggestion = "💡 Budget Suggestions:\n\n"
    
    if income > 0:
        saving_rate = ((income - expense) / income) * 100
        recommended_saving = income * 0.2
        
        suggestion += f"• Current saving rate: {saving_rate:.1f}%\n"
        suggestion += f"• Recommended saving: ₹{recommended_saving:.0f} (20% of income)\n"
        
        if saving_rate < 10:
            suggestion += "• Try to save at least 10% of your income\n"
        elif saving_rate >= 20:
            suggestion += "• Great job! You're saving well\n"
    
    if expense > 0:
        if expense > income:
            suggestion += "• ⚠️ You're spending more than earning!\n"
        suggestion += "• Track daily expenses to identify saving opportunities\n"
    
    if not transactions:
        suggestion = "Start tracking your income and expenses to get personalized budget suggestions!"
    
    messagebox.showinfo("Budget Suggestions", suggestion)

def show_chart(chart_type=None, parent_window=None):
    if parent_window is None:
        parent_window = main_window

    if not parent_window:
        return

    for widget in parent_window.winfo_children():
        if hasattr(widget, 'get_tk_widget'):  
            widget.get_tk_widget().destroy()
        elif str(type(widget)) == "<class 'matplotlib.backends.backend_tkagg.FigureCanvasTkAgg'>":
=======
def show_chart(chart_type=None):
    for widget in main_window.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
>>>>>>> Stashed changes
            widget.get_tk_widget().destroy()

    # Calculation
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')

    fig = Figure(figsize=(6, 4), dpi=80, facecolor='white')
    plot = fig.add_subplot(1, 1, 1)
    plot.set_facecolor('#f8f9fa')

    try:
        if chart_type == "Bar: Income vs Expense":
            if income == 0 and expense == 0:
                plot.text(0.5, 0.5, "No data available\nAdd some transactions first!", 
                         ha='center', va='center', transform=plot.transAxes, fontsize=12)
                plot.set_title("Income vs Expense")
            else:
                labels = ['Income', 'Expense']
                values = [income, expense]
                colors = ['#4CAF50', '#F44336']
                bars = plot.bar(labels, values, color=colors, alpha=0.8, width=0.6)
                plot.set_title("Income vs Expense", fontsize=14, fontweight='bold')
                plot.set_ylabel("Amount (₹)", fontsize=12)
                
                #label bar
                max_val = max(values) if max(values) > 0 else 1
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    plot.text(bar.get_x() + bar.get_width()/2, height + max_val*0.02,
                             f'₹{value:,.0f}', ha='center', va='bottom', fontweight='bold')

        elif chart_type == "Pie: Income vs Expense":
            if income == 0 and expense == 0:
                plot.text(0.5, 0.5, "No data available\nAdd some transactions first!", 
                         ha='center', va='center', transform=plot.transAxes, fontsize=12)
                plot.set_title("Income vs Expense Distribution")
            else:
                labels, values, colors = [], [], []
                if income > 0:
                    labels.append('Income')
                    values.append(income)
                    colors.append('#4CAF50')
                if expense > 0:
                    labels.append('Expense')
                    values.append(expense)
                    colors.append('#F44336')
                
                if values:
                    wedges, texts, autotexts = plot.pie(values, labels=labels, colors=colors, 
                                                       autopct='%1.1f%%', startangle=90, 
                                                       explode=[0.05] * len(values))
                    plot.set_title("Income vs Expense Distribution", fontsize=14, fontweight='bold')
                    
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')

        elif chart_type == "Bar: Category-wise Expense":
            category_totals = {}
            for t in transactions:
                if t['type'] == 'Expense':
                    cat = t['category']
                    category_totals[cat] = category_totals.get(cat, 0) + t['amount']

            if category_totals:
                sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
                categories, values = zip(*sorted_categories)
                
                colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
                bars = plot.bar(categories, values, color=colors, alpha=0.8)
                plot.set_title("Expense by Category", fontsize=14, fontweight='bold')
                plot.set_ylabel("Amount (₹)", fontsize=12)
                plot.tick_params(axis='x', rotation=45)
                
                max_val = max(values)
                for bar, value in zip(bars, values):
                    plot.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_val*0.02,
                             f'₹{value:,.0f}', ha='center', va='bottom', fontweight='bold')
            else:
                plot.text(0.5, 0.5, "No expense data available\nAdd some expenses first!", 
                         ha='center', va='center', transform=plot.transAxes, fontsize=12)
                plot.set_title("Expense by Category")

        elif chart_type == "Line: Income Over Time":
            income_data = [(t['date'], t['amount']) for t in transactions if t['type'] == 'Income']
            if income_data:
                income_data.sort(key=lambda x: x[0])
                dates, amounts = zip(*income_data)
                
                from datetime import datetime
                date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
                
                plot.plot(date_objects, amounts, color='#4CAF50', marker='o', 
                         linewidth=3, markersize=8, markerfacecolor='#2E7D32', alpha=0.8)
                plot.set_title("Income Over Time", fontsize=14, fontweight='bold')
                plot.set_ylabel("Amount (₹)", fontsize=12)
                plot.tick_params(axis='x', rotation=45)
                
                plot.grid(True, alpha=0.3, linestyle='--')
                
                plot.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
            else:
                plot.text(0.5, 0.5, "No income data available\nAdd some income first!", 
                         ha='center', va='center', transform=plot.transAxes, fontsize=12)
                plot.set_title("Income Over Time")

        elif chart_type == "Line: Expense Over Time":
            expense_data = [(t['date'], t['amount']) for t in transactions if t['type'] == 'Expense']
            if expense_data:
                expense_data.sort(key=lambda x: x[0])
                dates, amounts = zip(*expense_data)
                
                from datetime import datetime
                date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
                
                plot.plot(date_objects, amounts, color='#F44336', marker='o', 
                         linewidth=3, markersize=8, markerfacecolor='#C62828', alpha=0.8)
                plot.set_title("Expense Over Time", fontsize=14, fontweight='bold')
                plot.set_ylabel("Amount (₹)", fontsize=12)
                plot.tick_params(axis='x', rotation=45)
                
                plot.grid(True, alpha=0.3, linestyle='--')
                
                plot.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
            else:
                plot.text(0.5, 0.5, "No expense data available\nAdd some expenses first!", 
                         ha='center', va='center', transform=plot.transAxes, fontsize=12)
                plot.set_title("Expense Over Time")

        else:
<<<<<<< Updated upstream
            plot.text(0.5, 0.5, f"Chart type '{chart_type}' not recognized", 
                     ha='center', va='center', transform=plot.transAxes, fontsize=12)
            plot.set_title("Chart Error")

        plot.grid(True, alpha=0.3)
        fig.tight_layout(pad=2.0)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10, fill='both', expand=True)
        
        if not hasattr(parent_window, '_chart_canvas'):
            parent_window._chart_canvas = []
        parent_window._chart_canvas.append(canvas)
        
    except Exception as e:
        print(f"Error displaying chart: {e}")

        plot.text(0.5, 0.5, f"Error creating chart:\n{str(e)}", 
                 ha='center', va='center', transform=plot.transAxes, fontsize=10)
        plot.set_title("Chart Error")
        
        try:
            canvas = FigureCanvasTkAgg(fig, master=parent_window)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
        except:
            messagebox.showerror("Chart Error", f"Unable to display chart: {e}")

def open_chart_window():
    if not chart_selector:
        messagebox.showerror("Error", "Chart selector not initialized!")
        return
        
    chart_type = chart_selector.get()
    chart_win = tk.Toplevel(main_window)
    chart_win.title(f"Financial Chart - {chart_type}")
    chart_win.geometry("800x600")
    chart_win.configure(bg="#f5f5f5")
=======
            plot.text(0.5, 0.5, "No expense data", ha='center')
            
    elif chart_type == "Line: Income Over Time":
        dates = [t['date'] for t in transactions if t['type'] == 'Income']
        amounts = [t['amount'] for t in transactions if t['type'] == 'Income']
        plot.plot(dates, amounts, color='green', marker='o')
        plot.set_title("Income Over Time")
        plot.tick_params(axis='x', rotation=45)
>>>>>>> Stashed changes
    
    chart_win.resizable(True, True)
    
    title_label = tk.Label(chart_win, text=chart_type, font=("Segoe UI", 16, "bold"), 
                          bg="#f5f5f5", fg="#333")
    title_label.pack(pady=10)
    
    chart_frame = tk.Frame(chart_win, bg="#f5f5f5")
    chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    show_chart(chart_type, parent_window=chart_frame)
    
    button_frame = tk.Frame(chart_win, bg="#f5f5f5")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Button(button_frame, text="🔄 Refresh Chart", command=lambda: refresh_chart(chart_type, chart_frame), 
              bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ Close", command=chart_win.destroy, 
              bg="#757575", fg="white", font=("Segoe UI", 10, "bold")).pack(side="right", padx=5)
    
    tk.Button(button_frame, text="💾 Save Chart", command=lambda: save_chart(chart_type), 
              bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold")).pack(side="right", padx=5)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
def refresh_chart(chart_type, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    load_data()
    show_chart(chart_type, parent_frame)
    messagebox.showinfo("Chart Refreshed", "Chart data has been updated!")

def save_chart(chart_type):
    try:
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Chart As"
        )
        if filename:
            messagebox.showinfo("Save Chart", f"Chart saving feature will be implemented.\nSelected: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save chart: {e}")

=======
=======
>>>>>>> Stashed changes
    else:
        plot.text(0.5, 0.5, "Invalid Chart Type", ha='center')

    canvas = FigureCanvasTkAgg(fig, master=main_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

from playsound import playsound

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
def show_splash(username):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x250+500+300")
    splash.configure(bg="#1976D2")

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    tk.Label(splash, text="Loading Personal Finance Tracker", font=("Helvetica", 14, "bold"), bg="#1976D2", fg="white").pack(pady=30)
=======
=======
>>>>>>> Stashed changes
    label = ttk.Label(splash, text="", font=("Helvetica", 14))
    label.pack(pady=30)
>>>>>>> Stashed changes

    progress = ttk.Progressbar(splash, orient="horizontal", mode="determinate", length=300)
    progress.pack(pady=20)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    status_label = tk.Label(splash, text="Initializing...", font=("Helvetica", 10), bg="#1976D2", fg="white")
    status_label.pack(pady=10)

    def update_progress(value=0):
        status_messages = [
            "Loading user data...",
            "Connecting to database...",
            "Preparing dashboard...",
            "Almost ready...",
            "Welcome!"
        ]
        
=======
=======
>>>>>>> Stashed changes
    splash_texts = ["Loading.", "Loading..", "Loading...", "Loading...."]

    def animate_label(index=0):
        label.config(text=splash_texts[index % len(splash_texts)])
        splash.after(300, animate_label, index + 1)

    def play_splash_sound():
        try:
            playsound("splash.mp3")  # optional file
        except:
            pass

    splash.after(100, play_splash_sound)
    animate_label()

    def load_progress(value=0):
>>>>>>> Stashed changes
        if value >= 100:
            splash.destroy()
            show_main_app(username)
        else:
            progress['value'] = value
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            status_index = min(value // 20, len(status_messages) - 1)
            status_label.config(text=status_messages[status_index])
            splash.after(50, update_progress, value + 2)

    update_progress()

def listen_for_command():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            update_chat("Listening... Speak now!", sender="System")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
        update_chat("Processing...", sender="System")
        command = recognizer.recognize_google(audio).lower()
        process_voice_command(command)
        
    except sr.WaitTimeoutError:
        update_chat("Listening timed out. Please try again.", sender="System")
    except sr.UnknownValueError:
        update_chat("Sorry, could not understand the audio. Please speak clearly.", sender="System")
    except sr.RequestError as e:
        update_chat(f"Speech recognition service error: {e}", sender="System")
    except Exception as e:
        update_chat(f"Error: {e}", sender="System")

def process_voice_command(command):
    update_chat(command, sender="You")
    
    patterns = [
        r"add (income|expense) of (\d+(?:\.\d+)?) (?:for|from) (.+)",
        r"add (\d+(?:\.\d+)?) (income|expense) (?:for|from) (.+)",
        r"record (income|expense) (\d+(?:\.\d+)?) (.+)"
    ]
    
    transaction_added = False
    
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            groups = match.groups()
            
            if groups[0] in ['income', 'expense']:
                type_, amount, category = groups[0], groups[1], groups[2]
            else:
                amount, type_, category = groups[0], groups[1], groups[2]
            
            type_ = type_.capitalize()
            
            try:
                amount_float = float(amount)
                
                trans_type.set(type_)
                amount_entry.delete(0, tk.END)
                amount_entry.insert(0, str(amount_float))
                category_entry.delete(0, tk.END)
                category_entry.insert(0, category.strip())
                
                # Add transaction
                add_transactions()
                update_chat(f"Added {type_} of ₹{amount_float} for {category}.", sender="Assistant")
                transaction_added = True
                break
                
            except ValueError:
                update_chat("Invalid amount specified.", sender="Assistant")
                return
    
    if not transaction_added:
        if "show summary" in command or "show balance" in command:
            income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
            expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
            balance = income - expense
            response = f"Income: ₹{income:.2f}, Expense: ₹{expense:.2f}, Balance: ₹{balance:.2f}"
            update_chat(response, sender="Assistant")
            
        elif "open chart" in command or "show chart" in command:
            update_chat("Opening chart window...", sender="Assistant")
            open_chart_window()
            
        elif "budget suggestion" in command or "budget tip" in command:
            update_chat("Here are your budget suggestions...", sender="Assistant")
            show_budget_suggestion()
            
        else:
            suggestions = [
                "Try: 'Add income of 5000 for salary'",
                "Try: 'Add expense of 200 for food'",
                "Try: 'Show summary'",
                "Try: 'Open chart'",
                "Try: 'Budget suggestion'"
            ]
            response = "Sorry, I didn't understand that command.\n" + "\n".join(suggestions)
            update_chat(response, sender="Assistant")

def create_card(parent, title, variable, color):
    frame = tk.Frame(parent, bg=color, width=150, height=80, relief="raised", bd=2)
    frame.pack_propagate(False)
    frame.pack(side="left", padx=10, pady=5)

    title_label = tk.Label(frame, text=title, bg=color, fg="white", font=("Segoe UI", 10, "bold"))
    title_label.pack(pady=(10, 0))

    value_label = tk.Label(frame, textvariable=variable, bg=color, fg="white", font=("Segoe UI", 12, "bold"))
    value_label.pack(pady=(0, 10))

    return frame

def show_main_app(username):
    global main_window, trans_type, amount_entry, category_entry
    global income_var, expense_var, balance_var, chart_selector, chat_box

    main_window = tk.Tk()
    main_window.title("Personal Finance Tracker - Dashboard")
    main_window.geometry("1000x700")
    main_window.configure(bg="#263238")
    
    income_var = tk.StringVar(value="₹0")
    expense_var = tk.StringVar(value="₹0")
    balance_var = tk.StringVar(value="₹0")

    # Header
    header_frame = tk.Frame(main_window, bg="#37474F", height=60)
    header_frame.pack(fill="x", padx=10, pady=5)
    header_frame.pack_propagate(False)

    tk.Label(header_frame, text=f"Welcome back, {username}! 👋", font=("Segoe UI", 18, "bold"), fg="white", bg="#37474F").pack(side="left", padx=20, pady=15)

    # Logout button
    tk.Button(header_frame, text="Logout", command=lambda: [main_window.destroy(), show_login()], bg="#F44336", fg="white", font=("Segoe UI", 10, "bold")).pack(side="right", padx=20, pady=15)

    # Summary cards
    card_frame = tk.Frame(main_window, bg="#263238")
    card_frame.pack(pady=10)

    create_card(card_frame, "Total Income", income_var, "#4CAF50")
    create_card(card_frame, "Total Expense", expense_var, "#F44336")
    create_card(card_frame, "Balance", balance_var, "#2196F3")

    content_frame = tk.Frame(main_window, bg="#263238")
    content_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Transaction entry section
    entry_frame = tk.LabelFrame(content_frame, text="Add Transaction", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", fg="#000000", padx=15, pady=15)
    entry_frame.pack(side="left", fill="y", padx=5)

    tk.Label(entry_frame, text="Type:", font=("Segoe UI", 10, "bold"), bg="#ECEFF1").grid(row=0, column=0, sticky="w", pady=5)
    trans_type = ttk.Combobox(entry_frame, values=["Income", "Expense"], state="readonly", width=15)
    trans_type.current(0)
    trans_type.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(entry_frame, text="Amount (₹):", font=("Segoe UI", 10, "bold"), bg="#ECEFF1").grid(row=1, column=0, sticky="w", pady=5)
    amount_entry = ttk.Entry(entry_frame, width=15)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(entry_frame, text="Category:", font=("Segoe UI", 10, "bold"), bg="#ECEFF1").grid(row=2, column=0, sticky="w", pady=5)
    category_entry = ttk.Entry(entry_frame, width=15)
    category_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(entry_frame, text="Add Transaction", command=add_transactions, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=15)
    tk.Button(entry_frame, text="Export to Excel", command=export_to_excel, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, columnspan=2, pady=5)
    tk.Button(entry_frame, text="Export to PDF", command=export_to_pdf, bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, columnspan=2, pady=5)

    # Voice assistant section
    voice_frame = tk.LabelFrame(content_frame, text="Voice Assistant 🎙️", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=15, pady=15)
    voice_frame.pack(side="left", fill="both", expand=True, padx=5)

    chat_box = tk.Text(voice_frame, height=12, state="disabled", bg="white", wrap="word", font=("Segoe UI", 9))
    chat_scrollbar = ttk.Scrollbar(voice_frame, orient="vertical", command=chat_box.yview)
    chat_box.configure(yscrollcommand=chat_scrollbar.set)
    
    chat_box.pack(side="left", fill="both", expand=True)
    chat_scrollbar.pack(side="right", fill="y")

    voice_buttons_frame = tk.Frame(voice_frame, bg="#ECEFF1")
    voice_buttons_frame.pack(fill="x", pady=10)

    tk.Button(voice_buttons_frame, text="🎙️ Start Listening", command=listen_for_command, bg="#9C27B0", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    tk.Button(voice_buttons_frame, text="💡 Budget Tips", command=show_budget_suggestion, bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

    add_crud_buttons_to_main_window(content_frame)
    # Charts section
    chart_frame = tk.LabelFrame(content_frame, text="Financial Charts 📊", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=15, pady=15)
    chart_frame.pack(side="right", fill="y", padx=5)

    tk.Label(chart_frame, text="Select Chart Type:", font=("Segoe UI", 10, "bold"), bg="#ECEFF1").pack(pady=(0, 5))
    
=======
            splash.after(30, load_progress, value + 2)

    load_progress()
    
def show_main_app(username):
    global main_window, trans_type, amount_entry, category_entry
    global income_var, expense_var, balance_var, chart_selector

    main_window = tk.Tk()
=======
            splash.after(30, load_progress, value + 2)

    load_progress()
    
def show_main_app(username):
    global main_window, trans_type, amount_entry, category_entry
    global income_var, expense_var, balance_var, chart_selector

    main_window = tk.Tk()
>>>>>>> Stashed changes
    main_window.title("Dashboard - Personal Finance Tracker")
    main_window.geometry("900x650")
    main_window.configure(bg="#001F2D")

    tk.Label(main_window, text=f"Welcome, {username} 👋", font=("Segoe UI", 16, "bold"), fg="white", bg="#001F2D").pack(pady=15)

    card_frame = tk.Frame(main_window, bg="#001F2D")
    card_frame.pack(pady=5)

    income_var = tk.StringVar(value="₹ 0.00")
    expense_var = tk.StringVar(value="₹ 0.00")
    balance_var = tk.StringVar(value="₹ 0.00")

    def create_card(text, var, bg_color):
        card = tk.Frame(card_frame, bg=bg_color, padx=20, pady=10)
        tk.Label(card, text=text, font=("Segoe UI", 12, "bold"), fg="white", bg=bg_color).pack()
        tk.Label(card, textvariable=var, font=("Segoe UI", 14), fg="white", bg=bg_color).pack()
        return card

    create_card("Income", income_var, "#2E7D32").grid(row=0, column=0, padx=10)
    create_card("Expense", expense_var, "#C62828").grid(row=0, column=1, padx=10)
    create_card("Balance", balance_var, "#1565C0").grid(row=0, column=2, padx=10)

    entry_frame = tk.LabelFrame(main_window, text="Add Transaction", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", fg="#000000", padx=10, pady=10)
    entry_frame.pack(padx=20, pady=20, fill="x")

    tk.Label(entry_frame, text="Type:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
    trans_type = ttk.Combobox(entry_frame, values=["Income", "Expense"], state="readonly")
    trans_type.current(0)
    trans_type.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(entry_frame, text="Amount:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
    amount_entry = ttk.Entry(entry_frame)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(entry_frame, text="Category:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w")
    category_entry = ttk.Entry(entry_frame)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(entry_frame, text="Add Transaction", command=add_transactions, bg="#0288D1", fg="white", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

    chart_frame = tk.LabelFrame(main_window, text="Charts 📊", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=10, pady=10)
    chart_frame.pack(padx=20, pady=10, fill="x")

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    chart_selector = ttk.Combobox(chart_frame, values=[
        "Bar: Income vs Expense",
        "Pie: Income vs Expense", 
        "Bar: Category-wise Expense",
        "Line: Income Over Time",
        "Line: Expense Over Time"
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ], state="readonly", width=25)
=======
    ], state="readonly", width=30)
>>>>>>> Stashed changes
=======
    ], state="readonly", width=30)
>>>>>>> Stashed changes
    chart_selector.current(0)
    chart_selector.pack(pady=5)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Chart buttons
    chart_buttons_frame = tk.Frame(chart_frame, bg="#ECEFF1")
    chart_buttons_frame.pack(pady=10)
    
    tk.Button(chart_buttons_frame, text="📊 Open Chart Window", command=open_chart_window, 
              bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=2, fill="x")
    
    tk.Button(chart_buttons_frame, text="🔄 Refresh Preview", 
              command=lambda: show_chart(chart_selector.get(), preview_frame), 
              bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=2, fill="x")

    # Quick chart preview frame 
    preview_label = tk.Label(chart_frame, text="Chart Preview:", font=("Segoe UI", 10, "bold"), bg="#ECEFF1")
    preview_label.pack(pady=(10, 5))
    
    preview_frame = tk.Frame(chart_frame, bg="white", relief="sunken", bd=2, width=300, height=200)
    preview_frame.pack(pady=5, fill="both", expand=True)
    preview_frame.pack_propagate(False)  # Maintain size

    # Load data and initialize
    load_data()
    update_summary()
    
    # Show welcome message in chat
    update_chat("🎉 Welcome to your Personal Finance Dashboard!", sender="System")
    update_chat("Voice commands you can use:", sender="System")
    update_chat("• 'Add income of 5000 for salary'", sender="System")
    update_chat("• 'Add expense of 200 for food'", sender="System")
    update_chat("• 'Show summary' or 'Show balance'", sender="System")
    update_chat("• 'Open chart' or 'Show chart'", sender="System")
    update_chat("• 'Budget suggestion' or 'Budget tip'", sender="System")

    # Initial chart preview
    try:
        if chart_selector and len(transactions) > 0:
            show_chart(chart_selector.get(), preview_frame)
        else:
            placeholder_label = tk.Label(preview_frame, text="📊\n\nChart Preview\n\nAdd transactions to see charts", 
                                       font=("Segoe UI", 10), bg="white", fg="#666")
            placeholder_label.pack(expand=True)
    except Exception as e:
        print(f"Error showing initial chart: {e}")

    def on_chart_change(event):
        try:
            for widget in preview_frame.winfo_children():
                widget.destroy()
            # New chart
            if len(transactions) > 0:
                show_chart(chart_selector.get(), preview_frame)
            else:
                placeholder_label = tk.Label(preview_frame, text="📊\n\nNo Data\n\nAdd transactions first", 
                                           font=("Segoe UI", 10), bg="white", fg="#666")
                placeholder_label.pack(expand=True)
        except Exception as e:
            print(f"Error changing chart: {e}")
    
    chart_selector.bind('<<ComboboxSelected>>', on_chart_change)
    
=======
=======
>>>>>>> Stashed changes
    tk.Button(chart_frame, text="Show Chart", command=lambda: show_chart(chart_selector.get()), bg="#00796B", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

    voice_frame = tk.LabelFrame(main_window, text="Voice Assistant 🎙️", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=10, pady=10)
    voice_frame.pack(padx=20, pady=10, fill="x")
    tk.Label(voice_frame, text="(Voice command input box / response area here)").pack()

    load_data()
    update_summary()
    show_chart(chart_selector.get())
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    main_window.mainloop()

def load_data():
    global transactions
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    try:
        if current_user:
            db_transactions = get_transactions(current_user)
            transactions.clear()
            
            for row in db_transactions:
                transactions.append({
                    'id': row[0],
                    'type': row[1], 
                    'amount': row[2],
                    'category': row[3],
                    'note': row[4],
                    'date': row[5]
                })
        else:
            transactions.clear()
    except Exception as e:
        print(f"Error loading data: {e}")
        transactions.clear()
def export_to_excel():
    if not transactions:
        messagebox.showwarning("No Data", "No transactions to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return
=======
=======
>>>>>>> Stashed changes
    rows = get_transactions()
    transactions.clear()
    for row in rows:
        transactions.append({
            'id': row[0],
            'type': row[1],
            'amount': row[2],
            'category': row[3],
            'note': row[4],
            'date': row[5]
        })
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    try:
        df = pd.DataFrame(transactions)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Transactions exported to Excel:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export to Excel:\n{e}")
def export_to_pdf():
    if not transactions:
        messagebox.showwarning("No Data", "No transactions to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Transaction Report", ln=True, align="C")

        pdf.set_font("Arial", size=10)
        pdf.ln(10)

        headers = ["ID", "Type", "Amount", "Category", "Note", "Date"]
        col_widths = [10, 20, 20, 30, 50, 30]

        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1)
        pdf.ln()

        for txn in transactions:
            pdf.cell(col_widths[0], 10, str(txn["id"]), 1)
            pdf.cell(col_widths[1], 10, txn["type"], 1)
            pdf.cell(col_widths[2], 10, str(txn["amount"]), 1)
            pdf.cell(col_widths[3], 10, txn["category"], 1)
            pdf.cell(col_widths[4], 10, txn["note"][:25], 1)  
            pdf.cell(col_widths[5], 10, txn["date"], 1)
            pdf.ln()

        pdf.output(file_path)
        messagebox.showinfo("Success", f"Transactions exported to PDF:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export to PDF:\n{e}")
                
def main():
    # Initializing database
    try:
        create_table()
    except Exception as e:
        print(f"Database initialization error: {e}")
        messagebox.showerror("Database Error", "Failed to initialize database. Please check if the database module is working correctly.")
        return

    # Checking if user exists
    if not os.path.exists(CONFIG_FILE):
        # Show registration
        def create_initial_config():
            try:
                with open(CONFIG_FILE, "w") as f:
                    json.dump({"registered": True}, f)
            except Exception as e:
                print(f"Error creating config: {e}")
        
        root = tk.Tk()
        root.withdraw()  
        
        result = messagebox.askyesno("Welcome!", "Welcome to Personal Finance Tracker!\n\nThis is your first time using the app.\nWould you like to create an account?")
        
        if result:
            root.destroy()
            create_initial_config()
            show_register_window()
        else:
            root.destroy()
            return
    else:
        show_login()

# TO run the app
if __name__ == "__main__":
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    main()
=======
=======
>>>>>>> Stashed changes
    create_table

    # Check if user is already registered
    if not os.path.exists(CONFIG_FILE):
        # First time use - ask to register
        def on_first_register():
            with open(CONFIG_FILE, "w") as f:
                json.dump({"registered": True}, f)
            show_login()

        def show_register_window():
            reg_win = tk.Tk()
            reg_win.title("Register - Personal Finance Tracker")
            reg_win.geometry("300x250")

            ttk.Label(reg_win, text="Username").pack(pady=5)
            username_entry = ttk.Entry(reg_win)
            username_entry.pack(pady=5)

            ttk.Label(reg_win, text="Password").pack(pady=5)
            password_entry = ttk.Entry(reg_win, show="*")
            password_entry.pack(pady=5)

            def register_now():
                username = username_entry.get()
                password = password_entry.get()
                if not username or not password:
                    messagebox.showerror("Error", "Username and password cannot be empty.")
                    return
                if register_user(username, password):
                    messagebox.showinfo("Success", "Account registered. Please login.")
                    reg_win.destroy()
                    on_first_register()
                else:
                    messagebox.showerror("Error", "Username already exists.")

            ttk.Button(reg_win, text="Register", command=register_now).pack(pady=5)
            reg_win.mainloop()

        show_register_window()

    else:
<<<<<<< Updated upstream
        show_login()
>>>>>>> Stashed changes
=======
        show_login()
>>>>>>> Stashed changes
