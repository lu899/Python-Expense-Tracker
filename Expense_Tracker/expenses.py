from collections import defaultdict
from datetime import datetime
from utils import loadData, tabulateData, total, getCategories, loadBudget
import json

filename = "Expense_Tracker/expenses.json"
budgetfile = "Expense_Tracker/budget.json"

def createBudget():
    category = input("Enter category: ").lower()
    budget = int(input("Enter Monthly Budget: "))
    
    try:
        budget_data = loadBudget(budgetfile)
    except FileNotFoundError:
        budget_data = {}

    budget_data[category] = budget

    try:
        with open(budgetfile, "w") as file:
            json.dump(budget_data, file, indent=4)
        print("Budget added successfully!!")
    except IOError as e:
        print(f"Error while writing to file: {e}")

def addExpense():
    description = input("Enter description: ")
    category = input("Enter category: ")
    amount = int(input("Enter amount: "))
    dateAdded = datetime.now()
    print(dateAdded)

    try:
        expenses = loadData(filename)
    except FileNotFoundError:
        expenses = []

    if expenses:
        new_id = max(expense["id"] for expense in expenses) + 1
    else:
        new_id = 1

    expense = {'id': new_id,
            'description': description, 
            'category': category, 
            'amount': amount, 
            'date': dateAdded.strftime("%Y-%m-%d")}
    
    expenses.append(expense)

    try:
        with open(filename, "w") as file:
            json.dump(expenses, file, indent=4)
        print("Expense added successfully!!")
    except IOError as e:
        print(f"Error while writing to file: {e}")
    
def deleteExpense():
    viewExpenses()
    print()

    id = int(input("Enter expense id: "))
    expences = loadData(filename)

    del(expences[id-1])

    try:
        with open(filename, "w") as file:
            json.dump(expences, file, indent=4)
        print("Expense deleted successfully!!")
    except IOError as e:
        print(f"Error deleting expense: {e}")


def viewExpenses():
    expenses = loadData(filename)
    tabulateData(expenses)    

def viewCategory():
    expenses = loadData(filename)
    category = input("Enter category to view by: ").lower()
    data, categories = [], getCategories(expenses)

    if category in categories:
        for e in expenses:
            if e["category"].lower() == category:
                data.append(e)

        tabulateData(data)
        category_limit_checker(data, category)
    else:
        print("Sorry Category not available!!")

def monthlyReport(month):
    expenses = loadData(filename)
    data = []

    for e in expenses:
        m = datetime.strptime(e["date"], "%Y-%m-%d").strftime("%B").lower()
        if m == month:
            data.append(e)

    if data:
        tabulateData(data)
        monthy_limit_checker(data, month)
    else:
        print("No expenses for that month!!")

def fullReport():
    expenses = loadData(filename)
    months = defaultdict(list)

    for e in expenses:
        date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
        key = (date_obj.year, date_obj.month)
        months[key].append(e)
    
    sorted_keys = sorted(months.keys())

    for year, month in sorted_keys:
        m = datetime(year, month, 1).strftime("%B").lower()
        print(f"\n-------------------------------{m.upper()}---------------------------------\n")
        monthlyReport(m)

def category_limit_checker(expenses, category):
    data = loadBudget(budgetfile)
    
    if category.lower() in data:
        budget = data[category]*12
        if total(expenses) > budget:
            print(f"You are over your yearly budget by {total(expenses) - budget}!! Stop spending now!!")
    else:
        print(f"Set budget for {category}")
        createBudget()

def monthy_limit_checker(expenses, month):
    categories = getCategories(expenses)
    over_budget = []
    data = {}

    for category in categories:
        total = 0
        for e in expenses:
            if e["category"].lower() == category:
                total += e["amount"]
        data[category] = total
                
    budget = loadBudget(budgetfile)

    for key, value in data.items():
        if key in budget:
            if value > budget[key]:
                over_budget.append(key)
        else:
            print(f"Set Budget for {key}")
            createBudget()
    
    if over_budget:
        print(f"On {month.upper()} you were over budget in the following categories: {', '.join(over_budget)}")
