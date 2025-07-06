import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyttsx3
import speech_recognition as sr
import re
from tkcalendar import Calendar
import numpy as np


import json
import os

from database import create_table, register_user, validate_user, add_transactions as db_add_transaction, get_transactions

CONFIG_FILE = "user_config.json"

DATA_FILE = "transactions.json"

transactions = []

def hash_password(password):
    import hashlib
    return hashlib.sha26(password.encode()).hexdigest()

import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import json
import os
from PIL import Image, ImageTk

REMEMBER_FILE = "remember_user.json"

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyttsx3
import json
import os

REMEMBER_FILE = "remember_user.json"

chat_box = None

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
    username_entry.focus()
    

    tk.Label(login_win, text="Password", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    password_entry = ttk.Entry(login_win, show="*", font=("Segoe UI", 10))
    password_entry.pack(pady=5, ipady=3)
    username_entry.focus()

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

    login_win.bind('<Return>', lambda event: attempt_login())

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

def show_register_window():
    reg_win = tk.Tk()
    reg_win.title("Register - Personal Finance Tracker")
    reg_win.geometry("400x450")
    
    current_theme = {"bg": "#002B36", "fg": "white"}
    reg_win.configure(bg=current_theme["bg"])

    
    try:
        img = Image.open("logo1.png").resize((80, 80))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(reg_win, image=logo, bg=current_theme["bg"])
        logo_label.image = logo
        logo_label.pack(pady=10)
    except:
        pass

    # Title
    title_label = tk.Label(reg_win, text="", font=("Helvetica", 16, "bold"), bg=current_theme["bg"], fg=current_theme["fg"])
    title_label.pack(pady=5)

    def animate_title(index=0):
        full_text = "Create Your Finance Account"
        if index <= len(full_text):
            title_label.config(text=full_text[:index])
            reg_win.after(80, animate_title, index + 1)

    animate_title()

    tk.Label(
        reg_win,
        text="Voice-enabled personal finance tracker",
        font=("Helvetica", 10),
        bg=current_theme["bg"],
        fg="#AAAAAA"
    ).pack(pady=2)

    # Username and Password
    tk.Label(reg_win, text="Username", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=(20, 5))
    username_entry = ttk.Entry(reg_win, font=("Segoe UI", 10))
    username_entry.pack(pady=5, ipady=3)
    username_entry.focus()

    tk.Label(reg_win, text="Password", font=("Segoe UI", 10, "bold"), bg=current_theme["bg"], fg=current_theme["fg"]).pack(pady=5)
    password_entry = ttk.Entry(reg_win, show="*", font=("Segoe UI", 10))
    password_entry.pack(pady=5, ipady=3)
    username_entry.focus()

    def register_now():
        from database import register_user
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if register_user(username, password):
            messagebox.showinfo("Success", "Account created. Please login.")
            reg_win.destroy()
            with open("user_config.json", "w") as f:
                json.dump({"registered": True}, f)
            show_login()
        else:
            messagebox.showerror("Error", "Username already exists.")

    # Register Button
    reg_btn = tk.Button(
        reg_win,
        text="Register",
        command=register_now,
        bg="#00C853", fg="white",
        activebackground="#00A843",
        font=("Segoe UI", 10, "bold"),
        padx=10, pady=5,
        relief="flat"
    )
    reg_btn.pack(pady=20)

    # Theme Toggle
    def toggle_theme():
        if current_theme["bg"] == "#002B36":
            current_theme.update({"bg": "#f0f0f0", "fg": "black"})
        else:
            current_theme.update({"bg": "#002B36", "fg": "white"})

        reg_win.configure(bg=current_theme["bg"])
        for widget in reg_win.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton)):
                widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
            elif isinstance(widget, tk.Button):
                widget.config(bg="#00C853" if current_theme["bg"] == "#002B36" else "#00796B")

    theme_btn = tk.Button(
        reg_win,
        text="Toggle Theme",
        command=toggle_theme,
        bg="#455A64",
        fg="white",
        font=("Segoe UI", 9),
        relief="flat"
    )
    theme_btn.pack(pady=5)

    reg_win.mainloop()

    
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
def update_summary():
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    balance = income - expense

    income_var.set(f"₹ {income:.2f}")
    expense_var.set(f"₹ {expense:.2f}")
    balance_var.set(f"₹ {balance:.2f}")
    
def show_budget_suggestion():
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    suggestion = ""
    if income > 0:
        saving = income * 0.2
        suggestion += f"💡 Try saving at least ₹{saving:.0f} this month.\n"
    if expense > 5000:
        suggestion += "💡 Limit discretionary spending to ₹2000/month."
    messagebox.showinfo("Budget Suggestion", suggestion or "You're on track!")

    
def show_chart(chart_type=None, parent_window = None):
    if parent_window is None:
     parent_window = main_window

    for widget in parent_window.winfo_children():
     if isinstance(widget, FigureCanvasTkAgg):
        widget.get_tk_widget().destroy()


    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')

    fig = Figure(figsize=(4, 3), dpi=100)
    plot = fig.add_subplot(1, 1, 1)

    if chart_type == "Bar: Income vs Expense":
        labels = ['Income', 'Expense']
        values = [income, expense]
        plot.bar(labels, values, color=['green', 'red'])
        plot.set_title("Income vs Expense")
        plot.set_ylabel("Amount (₹)")

    elif chart_type == "Pie: Income vs Expense":
        labels = ['Income', 'Expense']
        values = [income, expense]
        colors = ['green', 'red']
        plot.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plot.set_title("Income vs Expense")

    elif chart_type == "Bar: Category-wise Expense":
        category_totals = {}
        for t in transactions:
            if t['type'] == 'Expense':
                cat = t['category']
                category_totals[cat] = category_totals.get(cat, 0) + t['amount']

        if category_totals:
            categories = list(category_totals.keys())
            values = list(category_totals.values())
            plot.bar(categories, values, color='orange')
            plot.set_title("Expense by Category")
            plot.set_ylabel("Amount (₹)")
            plot.tick_params(axis='x', rotation=45)
        else:
            plot.text(0.5, 0.5, "No expense data", ha='center')
            
    elif chart_type == "Line: Income Over Time":
        dates = [t['date'] for t in transactions if t['type'] == 'Income']
        amounts = [t['amount'] for t in transactions if t['type'] == 'Income']
        plot.plot(dates, amounts, color='green', marker='o')
        plot.set_title("Income Over Time")
        plot.tick_params(axis='x', rotation=45)
    
    elif chart_type == "Line: Expense Over Time":
        dates = [t['date'] for t in transactions if t['type'] == 'Expense']
        amounts = [t['amount'] for t in transactions if t['type'] == 'Expense']
        plot.plot(dates, amounts, color='red', marker='o')
        plot.set_title("Expense Over Time")
        plot.tick_params(axis='x', rotation=45)
        
    elif chart_type == "Line: Predicted Savings":
        days = list(range(len(transactions)))
        savings = [sum(t['amount'] if t['type']=="Income" else -t['amount'] for t in transactions[:i+1]) for i in days]
        
        if len(savings) >= 2:
            coef = np.polyfit(days, savings, 1)
            poly1d_fn = np.poly1d(coef)
            future_days = list(range(len(days)+7))
            plot.plot(future_days, poly1d_fn(future_days), linestyle='--', color='blue', label='Forecast')
            plot.plot(days, savings, color='green', label='Actual')
            
            plot.set_title("Projected Savings")
            plot.legend()

    else:
        plot.text(0.5, 0.5, "Invalid Chart Type", ha='center')

    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
    
def open_chart_window():
    chart_type = chart_selector.get()
    chart_win = tk.Toplevel(main_window)
    chart_win.title("Chart - " + chart_type)
    chart_win.geometry("500x400")
    chart_win.configure(bg="#ECEFF1")

    show_chart(chart_type, parent_window=chart_win)


from playsound import playsound

def show_splash(username):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x250+500+300")
    splash.configure(bg="#12F6F6")

    label = ttk.Label(splash, text="", font=("Helvetica", 14))
    label.pack(pady=30)

    progress = ttk.Progressbar(splash, orient="horizontal", mode="determinate", length=250)
    progress.pack(pady=20)

    splash_texts = ["Loading.", "Loading..", "Loading...", "Loading...."]

    def animate_label(index=0):
        label.config(text=splash_texts[index % len(splash_texts)])
        splash.after(300, animate_label, index + 1)

    def play_splash_sound():
        try:
            playsound("splash.mp3")  
        except:
            pass

    splash.after(100, play_splash_sound)
    animate_label()

    def load_progress(value=0):
        if value >= 100:
            splash.destroy()
            show_main_app(username)
        else:
            progress['value'] = value
            splash.after(30, load_progress, value + 2)

    load_progress()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            process_voice_command(command)
        except sr.WaitTimeoutError:
            messagebox.showwarning("Timeout", "Listening timed out.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Speech recognition service unavailable.")

def process_voice_command(command):
    update_chat(command, sender="You") 
    
    pattern = r"(add|record)\s+(income|expense)\s+(of|for)?\s*([\d.]+)\s*(from|for)?\s*(.*)?"
    match = re.search(pattern, command)

    if match:
        type_ = match.group(2).capitalize()
        amount = match.group(4)
        category = match.group(6) or "General"

        trans_type.set(type_)
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, amount)
        category_entry.delete(0, tk.END)
        category_entry.insert(0, category)

        add_transactions()
        update_chat(f"Added {type_} of ₹{amount} for {category}.", sender="Assistant")
        
    elif "go to dashboard" in command:
        update_chat("Opening dashboard...", sender="Assistant")
        show_main_app("User")
    
    elif "open chart" in command:
        update_chat("Opening chart...", sender="Assistant")
        open_chart_window()
    
    elif "show income summary" in command:
        update_chat(f"Income summary: {income_var.get()}", sender="Assistant")
        messagebox.showinfo("Income Summary", income_var.get())
    
    else:
        update_chat("Sorry, I didn't understand that command.", sender="Assistant")
        messagebox.showwarning("Unrecognized", "Sorry, command not recognized.")

    
def show_main_app(username):
    global main_window, trans_type, amount_entry, category_entry
    global income_var, expense_var, balance_var, chart_selector

    main_window = tk.Tk()
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
    
    top_section = tk.Frame(main_window, bg="#001F2D")
    top_section.pack(padx=20, pady=10, fill="x")
    
    entry_frame = tk.LabelFrame(top_section, text="Add Transaction", font=("Segoe UI", 12, "bold"),
                            bg="#ECEFF1", fg="#000000", padx=10, pady=10)
    entry_frame.pack(side="left", fill="both", expand=True, padx=5)


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

    chart_selector = ttk.Combobox(chart_frame, values=[
        "Bar: Income vs Expense",
        "Pie: Income vs Expense",
        "Bar: Category-wise Expense",
        "Line: Income Over Time",
        "Line: Expense Over Time"
    ], state="readonly", width=30)
    chart_selector.current(0)
    chart_selector.pack(side="left", padx=10)

    tk.Button(chart_frame, text="Show Chart", command=open_chart_window, bg="#00796B", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)
    
    calendar_frame = tk.LabelFrame(main_window, text="Transaction Calendar", font=("Segoe UI", 12, "bold"), bg="#ECEFF1", padx=10, pady=10)
    calendar_frame.pack(padx=20, pady=10, fill="x")
    cal = Calendar(calendar_frame, selectmode='day', background="#00796B", disabledbackground="gray", bordercolor="#00796B", headersbackground="#00796B", normalbackground="#f0f0f0", foreground='black', normalforeground='black')
    cal.pack()
    
    for t in transactions:
     cal.calevent_create(datetime.strptime(t['date'], "%Y-%m-%d"), t['category'], 'expense' if t['type'] == "Expense" else 'income')


    voice_frame = tk.LabelFrame(top_section, text="Voice Assistant 🎙️", font=("Segoe UI", 12, "bold"),
                            bg="#ECEFF1", padx=10, pady=10)
    voice_frame.pack(side="left", fill="both", expand=True, padx=5)
    
    global chat_box
    chat_box = tk.Text(voice_frame, height=10, state="disabled", bg="white", wrap="word")
    chat_box.pack(fill="both", expand=True, pady=(0, 10))
    
    def update_chat(msg, sender="You"):
        chat_box.config(state="normal")
        chat_box.insert(tk.END, f"{sender}: {msg}\n")
        chat_box.see(tk.END)  # Auto scroll to bottom
        chat_box.config(state="disabled")
    
    tk.Label(voice_frame, text="(Voice command input box / response area here)").pack()
    tk.Button(voice_frame, text="🎙️ Listen Command", command=listen_for_command,
          bg="#512DA8", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)
    
    

    load_data()
    update_summary()
    show_chart(chart_selector.get())
    tk.Button(main_window, text="💡 Get Budget Tip", command=show_budget_suggestion, bg="#FFC107", font=("Segoe UI", 10, "bold")).pack(pady=5)

    main_window.mainloop()

    
def load_data():
    global transactions
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

# Initial launch
if __name__ == "__main__":
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
        show_login()