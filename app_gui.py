import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import json
import os

from database import create_table, register_user, validate_user, add_transaction as db_add_transaction, get_transactions

DATA_FILE = "transactions.json"

transactions = []

def hash_password(password):
    import hashlib
    return hashlib.sha26(password.encode()).hexdigest()

def show_login():
    login_win = tk.Tk()
    login_win.title("Login - Personal Finance Tracker")
    login_win.geometry("300x250")

    ttk.Label(login_win, text="Username").pack(pady=5)
    username_entry = ttk.Entry(login_win)
    username_entry.pack(pady=5)

    ttk.Label(login_win, text="Password").pack(pady=5)
    password_entry = ttk.Entry(login_win, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            login_win.destroy()
            show_splash()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def attempt_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if register_user(username, password):
            messagebox.showinfo("Registered", "Account created. Please login.")
        else:
            messagebo.showerror("Error", "Username already exits.")
    
    ttk.Button(login_win, text="Login", command=attempt_login).pack(pady=5)
    ttk.Button(login_win, text="Register", command=attempt_register).pack(pady=5)

    login_win.mainloop()
    
def add_transaction():
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
    
def show_chart(chart_type=None):
    for widget in main_window.winfo_children():
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

    else:
        plot.text(0.5, 0.5, "Invalid Chart Type", ha='center')

    canvas = FigureCanvasTkAgg(fig, master=main_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x250+500+300")
    splash.configure(bg="#12F6F6")

    label = ttk.Label(splash, text="Loading Personal Finance Tracker...", font=("Helvetica", 14))
    label.pack(pady=30)

    progress = ttk.Progressbar(splash, orient="horizontal", mode="determinate", length=250)
    progress.pack(pady=20)

    def load_progress(value=0):
        if value >= 100:
            splash.destroy()
            show_main_app()
        else:
            progress['value'] = value
            splash.after(30, load_progress, value + 2)  # Simulate loading

    load_progress()  # Start loading
    
def show_main_app():
    global main_window, trans_type, amount_entry, category_entry
    global income_var, expense_var, balance_var, chart_selector

    main_window = tk.Tk()
    main_window.title("Voice Enabled Personal Finance Tracker")
    main_window.geometry("700x600")
    main_window.configure(bg="#004D4D")
    
    income_var = tk.StringVar(value="₹ 0.00")
    expense_var = tk.StringVar(value="₹ 0.00")
    balance_var = tk.StringVar(value="₹ 0.00")
    
    # Date
    today = datetime.now().strftime("%B %d, %Y")
    date_label = tk.Label(main_window, text=today, bg="#004D4D", fg="white", font=("Arial", 10, "bold"))
    date_label.place(x=10, y=10)

   # Summary
    summary_frame = ttk.LabelFrame(main_window, text="Summary", padding=10)
    summary_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(summary_frame, text="Income:").grid(row=0, column=0, sticky="w")
    ttk.Label(summary_frame, textvariable=income_var).grid(row=0, column=1, sticky="e")
    ttk.Label(summary_frame, text="Expense:").grid(row=1, column=0, sticky="w")
    ttk.Label(summary_frame, textvariable=expense_var).grid(row=1, column=1, sticky="e")
    ttk.Label(summary_frame, text="Balance:").grid(row=2, column=0, sticky="w")
    ttk.Label(summary_frame, textvariable=balance_var).grid(row=2, column=1, sticky="e")
    
    # Entry
    entry_frame = ttk.LabelFrame(main_window, text="Add Transaction", padding=10)
    entry_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(entry_frame, text="Type:").grid(row=0, column=0, sticky="w")
    trans_type = ttk.Combobox(entry_frame, values=["Income", "Expense"], state="readonly")
    trans_type.current(0)
    trans_type.grid(row=0, column=1)

    ttk.Label(entry_frame, text="Amount:").grid(row=1, column=0, sticky="w")
    amount_entry = ttk.Entry(entry_frame)
    amount_entry.grid(row=1, column=1)

    ttk.Label(entry_frame, text="Category:").grid(row=2, column=0, sticky="w")
    category_entry = ttk.Entry(entry_frame)
    category_entry.grid(row=2, column=1)

    add_btn = tk.Button(entry_frame, text="Add", command=add_transaction,
                        bg="#00796B", fg="white", activebackground="#004D40", font=("Arial", 12, "bold"))
    add_btn.grid(row=3, column=0, columnspan=2, pady=5)

    # Chart
    chart_frame = ttk.LabelFrame(main_window, text="Charts📊", padding=10)
    chart_frame.pack(padx=10, pady=10, fill="x")
    
    chart_selector = ttk.Combobox(
        chart_frame,
        values=[
            "Bar: Income vs Expense",
            "Pie: Income vs Expense",
            "Bar: Category-wise Expense",
            "Line: Income Over Time",
            "Line: Expense Over Time"
        ],
        state="readonly",
        width=30
    )    
    chart_selector.current(0)
    chart_selector.pack(side="left", padx=10)

    show_chart_btn = tk.Button(chart_frame, text="Show Chart", command=lambda: show_chart(chart_selector.get()),
                               bg="#00695C", fg="white", font=("Arial", 10, "bold"))
    show_chart_btn.pack(side="left", padx=10)

    # Voice Placeholder
    voice_frame = ttk.LabelFrame(main_window, text="Voice Assistant", padding=10)
    voice_frame.pack(padx=10, pady=10, fill="x")
    ttk.Label(voice_frame, text="(Voice commands here...)").pack()
    
    load_data()
    update_summary()
    show_chart(chart_selector.get())

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
    create_table()
    show_login()
