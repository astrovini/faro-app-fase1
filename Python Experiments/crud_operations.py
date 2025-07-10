from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# USERS TABLE EXAMPLES
# -----------------------------

def create_user(email, name):
    """Create a new user"""
    data = {"email": email, "name": name}
    response = supabase.table("users").insert(data).execute()
    print("User created:", response.data)
    return response.data[0] if response.data else None

def fetch_users():
    """Fetch all users"""
    response = supabase.table("users").select("*").execute()
    print("Users:", response.data)
    return response.data

def fetch_user_by_email(email):
    """Fetch a user by email"""
    response = supabase.table("users").select("*").eq("email", email).execute()
    if response.data:
        print("User found:", response.data[0])
        return response.data[0]
    else:
        print("User not found.")
        return None

def update_user_name(user_id, new_name):
    """Update a user's name"""
    response = supabase.table("users").update({"name": new_name}).eq("id", user_id).execute()
    print("Update response:", response.data)

def delete_user(user_id):
    """Delete a user by ID"""
    response = supabase.table("users").delete().eq("id", user_id).execute()
    print("Delete response:", response.data)

# -----------------------------
# EXPENSES TABLE EXAMPLES
# -----------------------------

def create_expense(user_id, amount, category, description, date=None):
    """Create an expense"""
    data = {
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "description": description
    }
    if date:
        data["date"] = date

    response = supabase.table("expenses").insert(data).execute()
    print("Expense created:", response.data)
    return response.data[0] if response.data else None

def fetch_expenses(user_id):
    """Fetch expenses for a specific user"""
    response = supabase.table("expenses").select("*").eq("user_id", user_id).execute()
    print(f"Expenses for user {user_id}:", response.data)
    return response.data

def update_expense(expense_id, updated_fields: dict):
    """Update an expense with specified fields"""
    response = supabase.table("expenses").update(updated_fields).eq("id", expense_id).execute()
    print("Update response:", response.data)

def delete_expense(expense_id):
    """Delete an expense by ID"""
    response = supabase.table("expenses").delete().eq("id", expense_id).execute()
    print("Delete response:", response.data)

# -----------------------------
# TEST FUNCTIONS
# -----------------------------

if __name__ == "__main__":
    # Example test calls

    # Create a user
    # user = create_user("test@example.com", "Test User")

    # Fetch all users
    # fetch_users()

    # Fetch user by email
    # fetch_user_by_email("test@example.com")

    # Update user name
    # update_user_name(user_id="<your-user-id>", new_name="Updated Name")

    # Delete user
    # delete_user(user_id="<your-user-id>")

    # Create an expense
    # create_expense(user_id="<your-user-id>", amount=20.5, category="Food", description="Pizza")

    # Fetch expenses for user
    # fetch_expenses(user_id="<your-user-id>")

    # Update an expense
    # update_expense(expense_id="<your-expense-id>", updated_fields={"category": "Updated Category"})

    # Delete an expense
    # delete_expense(expense_id="<your-expense-id>")
