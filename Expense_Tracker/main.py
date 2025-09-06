from expenses import addExpense, deleteExpense, viewExpenses, viewCategory, monthlyReport, fullReport, createBudget

def main():
    isRunning = True

    while isRunning:
        print("\n1. Create Monthly Budget")
        print("2. Add an Expense")
        print("3. View All Expenses")
        print('4. View Expense by Category')
        print("5. Delete an Expense")
        print("6. View Report for specific month")
        print("7. View full report")
        print("8. Exit\n")

        choice = int(input("What's your choice: "))

        match choice:
            case 1:
                createBudget()
            case 2:
                addExpense()
            case 3:
                viewExpenses()
            case 4:
                viewCategory()
            case 5:
                deleteExpense()
            case 6:
                month = input("Enter month: ").lower()
                monthlyReport(month)
            case 7:
                fullReport()
            case 8:
                isRunning = False
            case _:
                print("Invalid choice!1 Try Again!!")


if __name__ == "__main__":
    main()