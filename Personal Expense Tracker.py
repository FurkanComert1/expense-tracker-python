import turtle
import json
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self):
        self.expenses_file = "expenses.json"
        self.budget_file = "budget.json"
        self.valid_categories = ["Food", "Housing", "Transportation", "Shopping", "Entertainment", "Education", "Other"]

        self.expenses = self.load_data(self.expenses_file, [])
        self.budgets = self.load_data(self.budget_file, {})
    def load_data(self, filename, default_data):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return default_data
        return default_data

    def save_data(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_expense(self):
        while True:
            date_str = input("Please enter the date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")

        try:
            amount = float(input("Please enter the amount of your expense: "))
            category = input(f"Please enter the category ({', '.join(self.valid_categories)}): ").capitalize()
            if category not in self.valid_categories:
                category = "Other"
            description = input("Please enter a description of your expense: ")

            expense_id = len(self.expenses) + 1 if not self.expenses else max(exp["id"] for exp in self.expenses) + 1

            new_expense = {
                "id": expense_id,
                "date": date_str,
                "amount": amount,
                "category": category,
                "description": description
            }

            self.expenses.append(new_expense)
            self.save_data(self.expenses_file, self.expenses)
            print("Your expense is added successfully.")
        except ValueError:
            print("Invalid amount format.")

    def view_all_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return

        print(f"\n{'ID':<5} | {'Date':<12} | {'Amount':<10} | {'Category':<15} | {'Description'}")
        print("-" * 65)
        for exp in self.expenses:
            print(
                f"{exp['id']:<5} | {exp['date']:<12} | {exp['amount']:<10.2f} | {exp['category']:<15} | {exp['description']}")
    def delete_expense(self):
        self.view_all_expenses()
        if not self.expenses:
            return

        try:
            exp_id = int(input("\nEnter the ID of the expense you want to delete: "))
            for i, exp in enumerate(self.expenses):
                if exp["id"] == exp_id:
                    del self.expenses[i]
                    self.save_data(self.expenses_file, self.expenses)
                    print(f"Expense with ID {exp_id} deleted successfully.")
                    return
            print("Expense ID not found.")
        except ValueError:
            print("Invalid ID. Please enter a number.")
    def view_grouped_expenses(self):
        expenses_by_category = {}
        for exp in self.expenses:
            cat = exp["category"]
            if cat not in expenses_by_category:
                expenses_by_category[cat] = []
            expenses_by_category[cat].append(exp)

        for category, items in expenses_by_category.items():
            print(f"\nCategory: {category}")
            for item in items:
                print(f"Date: {item['date']}, Amount: {item['amount']}, Description: {item['description']}")
    def set_budget(self):
        category = input(f"Enter category for budget ({', '.join(self.valid_categories)}): ").capitalize()
        if category not in self.valid_categories:
            category = "Other"
        try:
            amount = float(input(f"Enter budget amount for {category}: "))
            self.budgets[category] = amount
            self.save_data(self.budget_file, self.budgets)
            print(f"Budget for {category} set to {amount} successfully.")
        except ValueError:
            print("Invalid budget amount.")

    def budget_alerts(self):
        if not self.budgets:
            print("No budgets set yet. Please set a budget first.")
            return

        category_totals = {}
        for exp in self.expenses:
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]

        for category, budget in self.budgets.items():
            total_spent = category_totals.get(category, 0)
            if total_spent > budget:
                print(f"ALARM: You exceeded the budget for {category}! Spent: {total_spent:.2f}, Budget: {budget:.2f}")
            else:
                print(f"OK: {category} is within budget. Spent: {total_spent:.2f}, Budget: {budget:.2f}")

    def draw_bar_chart(self):
        if not self.expenses:
            print("No expenses to draw a chart.")
            return

        category_totals = {}
        for exp in self.expenses:
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]

        wn = turtle.Screen()
        wn.title("Expense Bar Chart")

        t = turtle.Turtle()
        t.speed(0)

        max_height = 250
        bar_width = 40
        gap = 20
        x_start = -180

        max_value = max(category_totals.values(), default=0)
        scale = max_height / max_value if max_value else 1

        for category, total in category_totals.items():
            bar_height = total * scale
            t.penup()
            t.goto(x_start, -200)
            t.pendown()

            t.begin_fill()
            t.fillcolor("blue")
            t.left(90)
            t.forward(bar_height)
            t.right(90)
            t.forward(bar_width)
            t.right(90)
            t.forward(bar_height)
            t.left(90)
            t.end_fill()

            t.penup()
            t.goto(x_start + bar_width / 2, -210)
            t.write(category, align="center")

            x_start += bar_width + gap

        t.hideturtle()
        wn.mainloop()

    def menu(self):
        while True:
            print("""
            === Personal Expense Tracker ===
            1- Add Expense
            2- View All Expenses
            3- View Grouped Expenses
            4- Delete Expense
            5- Set Budget
            6- Budget Alerts
            7- Produce Bar Chart For Expenses
            8- Exit
            """)
            try:
                choice = int(input("Please select an option (1-8): "))
                if choice == 1:
                    self.add_expense()
                elif choice == 2:
                    self.view_all_expenses()
                elif choice == 3:
                    self.view_grouped_expenses()
                elif choice == 4:
                    self.delete_expense()
                elif choice == 5:
                    self.set_budget()
                elif choice == 6:
                    self.budget_alerts()
                elif choice == 7:
                    self.draw_bar_chart()
                elif choice == 8:
                    print("Exiting the application...")
                    break
                else:
                    print("Invalid choice. Please select between 1-8.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nProgram interrupted by user. Exiting...")
                break

if __name__ == "__main__":
    app = ExpenseTracker()
    app.menu()