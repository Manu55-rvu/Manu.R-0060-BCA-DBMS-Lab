from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'prati',
    'database': 'expenses_db',
    'port': 3306
}
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                transaction_id, 
                title, 
                type, 
                category, 
                CAST(amount AS CHAR) AS amount, 
                DATE_FORMAT(transaction_date, '%Y-%m-%d') AS transaction_date, 
                notes 
            FROM transactions 
            ORDER BY transaction_date DESC, transaction_id DESC
        """)
        transactions = cursor.fetchall()
        cursor.execute("SELECT type, SUM(amount) AS total FROM transactions GROUP BY type")
        summary_rows = cursor.fetchall()
        total_income = 0.0
        total_expense = 0.0
        for row in summary_rows:
            if row['type'] == 'Income':
                total_income = float(row['total'])
            elif row['type'] == 'Expense':
                total_expense = float(row['total'])
        balance = total_income - total_expense
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'transactions': transactions,
            'summary': {
                'income': total_income,
                'expense': total_expense,
                'balance': balance
            }
        }), 200
    except Error as e:
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json() or request.form
    title = data.get('title')
    tx_type = data.get('type')
    category = data.get('category')
    amount = data.get('amount')
    transaction_date = data.get('transaction_date')
    notes = data.get('notes', '')

    if not title or not category or not amount or not transaction_date or not tx_type:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO transactions (title, type, category, amount, transaction_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, tx_type, category, float(amount), transaction_date, notes))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Transaction added successfully'}), 201
    except Error as e:
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Deleted successfully'}), 200
    except Error as e:
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)