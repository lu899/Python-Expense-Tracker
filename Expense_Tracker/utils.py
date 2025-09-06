import json, tabulate

def total(expenses):
    total = 0
    amount = [e["amount"] for e in expenses]
    for t in amount:
        total += t
    return total

def loadData(filename):
    with open(filename, "r") as file:
        expenses = json.load(file)
    return expenses

def loadBudget():
    with open("budget.json", "r") as file:
        budget_data = json.load(file)
    return budget_data

def tabulateData(expenses):
    table = [[e["id"], e["description"], e["category"], e["amount"], e["date"]] for e in expenses]
    headers = ["Id", "Description", "Category", "Amount", "Date"]

    print(tabulate.tabulate(table, headers=headers, tablefmt="grid"))
    print(f"Total Expenses: {total(expenses)}")

def getCategories(expenses):
    categories = []
    for e in expenses:
        if e["category"].lower() not in categories:
            categories.append(e["category"].lower())
    
    return categories