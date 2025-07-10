import time
from user import User

current_user = None

def signup():
    global current_user
    email = input("Enter email: ")
    name = input("Enter name: ")
    current_user = User.create(email, name)
    if current_user:
        print(f"Signed up and logged in as {current_user.name} ({current_user.email})")
    else:
        print("Signup failed.")

def login():
    global current_user
    email = input("Enter your email to log in: ")
    user = User.get_by_email(email)
    if user:
        current_user = user
        print(f"Logged in as {current_user.name} ({current_user.email})")
    else:
        print("User not found. Please sign up first.")

def logout():
    global current_user
    if current_user:
        print(f"Logged out from {current_user.email}")
        current_user = None
    else:
        print("No user is currently logged in.")

def main_menu():
    while True:
        if current_user is None:
            print("""
                === Expense Tracker ===
                1. Sign Up
                2. Login
                3. Exit
                """)
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    signup()
                case "2":
                    login()
                case "3":
                    print("Exiting...")
                    time.sleep(1)
                    break
                case _:
                    print("Invalid option, try again.")
        else:
            print("""
                === Expense Tracker Menu ===
                1. Create Expense
                2. View My Expenses
                3. Logout
                4. Exit
                """)
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    amount = float(input("Amount: "))
                    category = input("Category: ")
                    description = input("Description: ")
                    custom_date = input("Custom date (YYYY-MM-DDTHH:MM:SSZ) or leave blank: ")
                    date = custom_date if custom_date.strip() else None
                    current_user.create_expense(amount, category, description, date)
                case "2":
                    current_user.fetch_expenses()
                case "3":
                    logout()
                case "4":
                    print("Exiting...")
                    time.sleep(1)
                    break
                case _:
                    print("Invalid option, try again.")

if __name__ == "__main__":
    main_menu()