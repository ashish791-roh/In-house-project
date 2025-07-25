import sqlite3
from database import create_table, add_transaction

def main():
    create_table()

    while True:
        print("\nPersonal Finance Tracker\n")
        print("Press 1 to add income")
        print("Press 2 to add expenses")
        print("Press 3 for exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter your income amount: ₹"))
            category = input("Enter your source (e.g., salary, gifts, etc) of income: ")
            note = input("Optional note: ")
            add_transaction("Income", amount, category, note)
            print("Income added successfully.")

        elif choice == "2":
            amount = float(input("Enter your expenses: ₹"))
            category = input("Enter category of expenses (e.g., bills, rent, etc): ")
            note = input("Optional note: ")
            add_transaction("Expenses", amount, category, note)
            print("Expenses added successfully.")

        elif choice == "3":
            print("Exiting, Bye")
            break

        else:
            print("Invalid choice, please select 1, 2 or 3")

if __name__ == "__main__":
    main()