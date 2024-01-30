from collections import defaultdict
from datetime import datetime
from random import randint
from db.database import Database
from resources.summary_dashboard_ui import Ui_Form
from PySide6 import QtCharts
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class SummaryDashboard(QWidget, Ui_Form):
    def __init__(self, db: Database):
        super().__init__()

        self.db = db

        self.setupUi(self)
        self._init_UI()

    def _init_UI(self):
        # Balance frame
        self.plot_monthly_balance()

        # Monthly expense frame
        self.plot_monthly_expenses(self.get_monthly_expense())

    def plot_monthly_expenses(self, monthly_expenses):
        fig, ax = plt.subplots()

        months = list(monthly_expenses.keys())

        categories = set()
        for expenses in monthly_expenses.values():
            categories.update(expenses.keys())

        x = range(len(months))

        bar_width = 0.35

        for i, category in enumerate(categories):
            amounts = [expenses.get(category, 0)
                       for expenses in monthly_expenses.values()]
            ax.bar([pos + bar_width * i for pos in x],
                   amounts, bar_width, label=category)

        ax.set_xticks(
            [pos + bar_width * (len(categories) - 1) / 2 for pos in x])
        # Hónapok megjelenítése elforgatva
        ax.set_xticklabels(months, rotation=45)

        fig.patch.set_facecolor('#313a46')

        ax.set_facecolor('#313a46')
        ax.set_xlabel('Months', color='white')
        ax.set_ylabel('Expenses', color='white')
        ax.set_title('Monthly Expenses by Category', color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        ax.legend()

        canvas = FigureCanvas(fig)
        monthly_expense_layout = QVBoxLayout(self.MonthlyExpenseFrame)
        monthly_expense_layout.addWidget(canvas)

    def get_monthly_expense(self):
        transactions = self.db.get_all_transactions()
        categories = self.db.get_all_categories()

        monthly_expenses = defaultdict(lambda: defaultdict(int))

        for data in transactions:
            date = data['date']
            category = data['category']
            amount = data['amount']

            year_month = datetime.strptime(date, '%Y.%m.%d').strftime('%Y.%m')

            monthly_expenses[year_month][category] += amount

        return monthly_expenses

    def calculate_monthly_balance(self):
        transactions = self.db.get_all_transactions()

        balance = defaultdict(float)
        previous_balance = 0.0

        for data in transactions:
            print(f"prev balance: {previous_balance}")
            date = datetime.strptime(data['date'], '%Y.%m.%d')
            amount = data['amount']

            year_month = date.replace(day=1)

            balance[year_month] += float(amount)
            previous_balance = balance[year_month]

        return balance

    def plot_monthly_balance(self):
        balance_data = self.calculate_monthly_balance()

        sorted_dates = sorted(balance_data.keys())
        months = [date.strftime('%Y.%m')
                  for date in sorted(balance_data.keys())]
        balances = [balance_data[date] for date in sorted_dates]

        fig, ax = plt.subplots()

        ax.plot(months, balances, marker='o', color='#00FF00')
        fig.patch.set_facecolor('#313a46')

        ax.set_facecolor('#313a46')
        ax.set_xlabel('Months', color='white')
        ax.set_ylabel('Balance', color='white')
        ax.set_title('Balance Over Months')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Hozzunk létre egy canvas-t és adjuk hozzá a layout-hoz
        canvas = FigureCanvas(fig)

        balance_layout = QVBoxLayout(self.balanceChartFrame)
        balance_layout.addWidget(canvas)
