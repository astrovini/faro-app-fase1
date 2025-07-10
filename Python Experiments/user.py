from config import supabase
from expense import Expense

class User:
    def __init__(self, id, email, name, created_at):
        self.id = id
        self.email = email
        self.name = name
        self.created_at = created_at

    @classmethod
    def create(cls, email, name):
        data = {"email": email, "name": name}
        response = supabase.table("users").insert(data).execute()
        if response.data:
            user_record = response.data[0]
            print(f"User {user_record['name']} created.")
            return cls(
                id=user_record['id'],
                email=user_record['email'],
                name=user_record['name'],
                created_at=user_record['created_at']
            )
        else:
            print("User creation failed.")
            return None

    @classmethod
    def get_by_email(cls, email):
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            user_record = response.data[0]
            return cls(
                id=user_record['id'],
                email=user_record['email'],
                name=user_record['name'],
                created_at=user_record['created_at']
            )
        else:
            return None

    def create_expense(self, amount, category, description, date=None):
        data = {
            "user_id": self.id,
            "amount": amount,
            "category": category,
            "description": description
        }
        if date:
            data["date"] = date

        response = supabase.table("expenses").insert(data).execute()
        if response.data:
            print(f"Expense {response.data[0]['id']} created.")
        else:
            print("Failed to create expense.")

    def fetch_expenses(self):
        response = supabase.table("expenses").select("*").eq("user_id", self.id).execute()
        expenses = [Expense.from_record(record) for record in response.data]
        print(f"\nExpenses for {self.name}:\n")
        for expense in expenses:
            print(expense)