from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from utils import loadData, getCategories, loadBudget, categoryData

expences = loadData("Expense_Tracker/expenses.json")
budgets = loadBudget("Expense_Tracker/budget.json")
categories = getCategories(expences)
category_data = categoryData(expences, categories)

def fullReport():
    # Total Monthly Report
    months = defaultdict(list)
    data = {}

    for e in expences:
        date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
        key = (date_obj.year, date_obj.month)
        months[key].append(e)
    sorted_keys = sorted(months.keys())

    for year, month in sorted_keys:
        total = 0
        m = datetime(year, month, 1).strftime("%B").title()
        for e in months[(year, month)]:
            total += e["amount"]
        data[m] = total      

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Monthly Expense Report (Bar Chart)
    axs[0].bar(data.keys(), data.values(), color='#9db4cf')
    axs[0].set_title("Monthly Expense Report", fontsize=16, fontweight='bold')
    axs[0].set_xlabel("Months", fontsize=12)
    axs[0].set_ylabel("Amount Spent (Kshs)", fontsize=12)
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].grid(axis='y', linestyle='--', alpha=0.5)

    # Categories report (Pie Chart)
    cmap = plt.get_cmap('tab20')
    custom_colors = [cmap(i) for i in range(len(categories))]
    wedges, texts, autotexts = axs[1].pie(
        category_data.values(), autopct='%1.1f%%', startangle=90, colors=custom_colors, textprops={'fontsize': 10}
    )
    axs[1].legend(wedges, category_data.keys(), title="Categories", loc="lower center", bbox_to_anchor=(0.5, -0.3), fontsize=9, ncol=2)
    axs[1].set_title("% Spent in Each Category", fontsize=16, fontweight='bold')

    # Categories Over Budget (Bar Chart)
    OverBudget = {}
    for key, value in budgets.items():
        budget = value*12
        if key.title() in category_data:
            if category_data[key.title()] > budget:
                OverBudget[key.title()] = category_data[key.title()] - budget
    bar_container = axs[2].bar(OverBudget.keys(), OverBudget.values(), color="#e57373")
    axs[2].set_xlabel("Category", fontsize=12)
    axs[2].set_ylabel("Overbudget (Kshs)", fontsize=12)
    axs[2].set_title("Categories Over Budget", fontsize=16, fontweight='bold')
    axs[2].bar_label(bar_container, fmt='{:,.0f}')
    axs[2].tick_params(axis='x', rotation=30)
    axs[2].grid(axis='y', linestyle='--', alpha=0.5)

    fig.suptitle("Full Expense Report", fontsize=20, fontweight='bold')
    plt.tight_layout(rect=[0.05, 0, 0.97, 0.95])  # Add more space on the left
    plt.subplots_adjust(wspace=0.3, left=0.07, bottom=0.22, top=0.88, right=0.97)  # Increase left margin
    plt.show()