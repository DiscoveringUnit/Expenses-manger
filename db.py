import sqlite3
import os
from decimal import Decimal
import datetime

filepath = "data/expenses.db"

os.makedirs("data", exist_ok=True) # creates folder, instead of "data" there can be actual path where you want dir to be created
conn = sqlite3.connect(filepath) # creates connection to db and file itself

def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        logged_at TEXT NOT NULL,
        expense_date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        currency TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT,
        type TEXT NOT NULL,
        description TEXT
)
""")
    
init_db()

def add_expense(expense_date, payment_method, amount, currency, category, expense_type, description= None, sub_category = None):

    logged_at = datetime.datetime.now().isoformat()
    amount_cents = int(amount*100)

    conn.execute("""
    INSERT INTO expenses (
        logged_at, expense_date, payment_method, amount_cents, currency, category, sub_category, type, description)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?);
""",
    (logged_at, expense_date, payment_method, amount_cents, currency, category, sub_category, expense_type, description)
)
    conn.commit()

def get_expenses():
        rows = conn.execute ("""SELECT * FROM expenses""").fetchall()
        return rows

def delete_expense(expense_id):
    conn.execute("""
    DELETE FROM expenses WHERE id = ?                
""",
    (expense_id,)
)
    conn.commit()

def update_expense(expense_id, expense_date, payment_method, amount, currency, category, expense_type, description= None, sub_category = None):

    amount_cents = int(amount*100)
    
    conn.execute("""
    UPDATE expenses
    SET 
        expense_date = ?,
        payment_method = ?,
        amount_cents = ?,
        currency = ?,
        category = ?,
        sub_category = ?,
        type = ?,
        description = ?
    WHERE id = ?               
""",
    (expense_date, payment_method, amount_cents, currency, category, sub_category, expense_type, description, expense_id)
)
    conn.commit()

#add_expense(expense_date="2026-07-04", payment_method="SEB_card", amount=Decimal(170.34), currency="USD", category="Subscription", expense_type="other")