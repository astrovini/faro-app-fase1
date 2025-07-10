class Expense:
    def __init__(self, id, user_id, amount, category, description, date):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    @classmethod
    def from_record(cls, record):
        return cls(
            id=record['id'],
            user_id=record['user_id'],
            amount=record['amount'],
            category=record['category'],
            description=record['description'],
            date=record['date']
        )

    def __str__(self):
        return f"{self.date} | {self.category} | {self.description} | ${self.amount}"