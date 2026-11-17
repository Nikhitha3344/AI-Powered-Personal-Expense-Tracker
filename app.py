from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Gemini API Key Loaded:", bool(os.getenv("GEMINI_API_KEY")))

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="expense_tracker"
)

print("MySQL Database Connected Successfully!")



@app.route("/")
def home():
    print("HOME PAGE OPENED")
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    transactions = cursor.fetchall()
    df = pd.DataFrame(transactions)

    print("\nTransaction Data:")
    print(df)


    # Filter only Expense transactions
    expense_df = df[df["type"] == "Expense"]

    # Calculate total expenses by category
    category_summary = expense_df.groupby("category")["amount"].sum()

    print("\nExpenses by Category:")
    print(category_summary)
    if not category_summary.empty:
        highest_category = category_summary.idxmax()
        highest_amount = category_summary.max()

        print("\nHighest Spending Category:")
        print(highest_category, highest_amount)
    else:
        print("\nNo expense transactions found.")


    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expenses
        FROM transactions
    """)

    totals = cursor.fetchone()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
    """)

    category_data = cursor.fetchall()

    category_labels = [row["category"] for row in category_data]
    category_amounts = [float(row["total"]) for row in category_data]


    total_income = float(totals["total_income"] or 0)
    total_expenses = float(totals["total_expenses"] or 0)
    balance = total_income - total_expenses

    cursor.close()

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        category_labels=category_labels,
        category_amounts=category_amounts
    )



@app.route("/test")
def test():
    return "Flask Backend is Working!"

@app.route("/gemini-test")
def gemini_test():
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Say hello in one sentence."
    )
    return response.text

@app.route("/ai-suggestions")
def ai_suggestions():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
    """)

    expense_data = cursor.fetchall()
    cursor.close()

    if not expense_data:
        return "No expense data available."

    expense_summary = "\n".join(
        [f"{item['category']}: ₹{float(item['total']):.2f}"
         for item in expense_data]
    )

    prompt = f"""
    Analyse these expense categories:
    {expense_summary}

    Give 3 simple and practical suggestions
    to help reduce unnecessary spending.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expenses
        FROM transactions
    """)

    totals = cursor.fetchone()
    cursor.close()

    total_income = float(totals["total_income"] or 0)
    total_expenses = float(totals["total_expenses"] or 0)
    balance = total_income - total_expenses

    prompt = f"""
    You are a helpful personal finance assistant.

    User's financial summary:
    Total Income: ₹{total_income}
    Total Expenses: ₹{total_expenses}
    Balance: ₹{balance}

    Answer the user's question using this data:
    {user_message}

    Give simple and clear answers.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return jsonify({"reply": response.text})

@app.route("/add", methods=["POST"])
def add_transaction():
    description = request.form.get("description")
    amount = request.form.get("amount")
    category = request.form.get("category")
    type = request.form.get("type")
    date = request.form.get("date")

    cursor = db.cursor()

    query = """
    INSERT INTO transactions
    (description, amount, category, type, date)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (description, amount, category, type, date)

    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return "Transaction Saved Successfully!"

@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    cursor = db.cursor()

    query = "DELETE FROM transactions WHERE id = %s"
    cursor.execute(query, (transaction_id,))

    db.commit()
    cursor.close()

    return "Transaction Deleted Successfully!"

@app.route("/update/<int:transaction_id>", methods=["POST"])
def update_transaction(transaction_id):
    description = request.form.get("description")
    amount = request.form.get("amount")
    category = request.form.get("category")
    type = request.form.get("type")
    date = request.form.get("date")

    cursor = db.cursor()

    query = """
    UPDATE transactions
    SET description = %s, amount = %s, category = %s,
        type = %s, date = %s
    WHERE id = %s
    """

    values = (description, amount, category, type, date, transaction_id)

    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return "Transaction Updated Successfully!"

if __name__ == "__main__":
    app.run(debug=True)
