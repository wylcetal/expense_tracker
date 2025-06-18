from expense import Expense
import calendar
import datetime
import getpass
from export_data import export_data


def main():
    print("Welcome to the Expense Tracker")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Menú principal
    while True:
        print("\n=== EXPENSE TRACKER MENU ===")
        print("1. Add Expense")
        print("2. Summarize Expenses")
        print("3. Export Data")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            # Get user input for expense
            expense = get_user_expense()
            # Write their expense to a file
            save_expense_to_file(expense, expense_file_path)

        elif choice == "2":
            # Read file and summarize expenses
            summarize_expenses(expense_file_path, budget)

        elif choice == "3":
            export_menu(expense_file_path)

        elif choice == "4":
            print("Thank you for using Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


def export_menu(expense_file_path):
    """
    Menú para exportar datos
    """
    while True:
        print("\n=== EXPORT MENU ===")
        print("1. Export to Google Sheets")
        print("2. Export to MySQL")
        print("3. Export to Supabase")
        print("4. Back to Main Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            sheet_name = (
                input("Enter Google Sheet name (default: Expense Tracker): ")
                or "Expense Tracker"
            )
            export_data(expense_file_path, "gsheets", sheet_name=sheet_name)

        elif choice == "2":
            host = input("Enter MySQL host (default: localhost): ") or "localhost"
            user = input("Enter MySQL user (default: root): ") or "root"
            password = getpass.getpass("Enter MySQL password: ")
            database = (
                input("Enter MySQL database name (default: expense_tracker): ")
                or "expense_tracker"
            )

            export_data(
                expense_file_path,
                "mysql",
                host=host,
                user=user,
                password=password,
                database=database,
            )

        elif choice == "3":
            table_name = input("Enter table name (default: expenses): ") or "expenses"

            export_data(
                expense_file_path,
                "supabase",
                table_name=table_name,
            )

        elif choice == "4":
            return

        else:
            print("Invalid choice. Please try again.")


def get_user_expense():
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = ["🍔 Food", "🏠 Home", "💻 Work", "🎉 Fun", "🎵 Music"]

    while True:
        print("Select a category:")
        for i, category in enumerate(expense_categories):
            print(f"  {i + 1}. {category}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category number. Please try again!.")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print("🎯 Summarizing User Expenses")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():  # Ignorar líneas vacías
                name, amount, category = line.strip().split(",")
                line_expense = Expense(
                    name=name,
                    category=category,
                    amount=float(amount),
                )
                expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses by Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([expense.amount for expense in expenses])
    print(f"💰 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
