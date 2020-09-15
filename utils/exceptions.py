class NoExpensesError(Exception):
    def __init__(self, category):
        self.category = category

    def __str__(self):
        return f"No expenses were found for {self.category}"
