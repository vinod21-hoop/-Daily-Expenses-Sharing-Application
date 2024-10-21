from flask import Flask, request, jsonify, send_file
import json
from datetime import datetime
import os
import csv
import io

app = Flask(__name__)

DATA_FILE = 'expenses_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'users': [], 'expenses': [], 'expense_splits': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/users', methods=['POST'])
def create_user():
    data = load_data()
    new_user = request.json
    if not new_user or 'name' not in new_user or 'email' not in new_user or 'mobile' not in new_user:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check for unique email and mobile
    if any(user['email'] == new_user['email'] for user in data['users']):
        return jsonify({'error': 'Email already exists'}), 409
    if any(user['mobile'] == new_user['mobile'] for user in data['users']):
        return jsonify({'error': 'Mobile number already exists'}), 409

    new_user['id'] = len(data['users']) + 1
    data['users'].append(new_user)
    save_data(data)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = load_data()
    user = next((user for user in data['users'] if user['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = load_data()
    new_expense = request.json
    if not new_expense or 'description' not in new_expense or 'amount' not in new_expense or 'paid_by' not in new_expense or 'split_method' not in new_expense or 'splits' not in new_expense:
        return jsonify({'error': 'Missing required fields'}), 400

    if new_expense['split_method'] not in ['EQUAL', 'EXACT', 'PERCENTAGE']:
        return jsonify({'error': 'Invalid split method'}), 400

    if new_expense['split_method'] == 'PERCENTAGE' and sum(split['value'] for split in new_expense['splits']) != 100:
        return jsonify({'error': 'Percentage splits must sum to 100'}), 400

    new_expense['id'] = len(data['expenses']) + 1
    new_expense['created_at'] = datetime.now().isoformat()
    data['expenses'].append(new_expense)

    for split in new_expense['splits']:
        split_entry = {
            'id': len(data['expense_splits']) + 1,
            'expense_id': new_expense['id'],
            'user_id': split['user_id'],
            'amount': split['value'] if new_expense['split_method'] in ['EXACT', 'PERCENTAGE'] else new_expense['amount'] / len(new_expense['splits']),
            'percentage': split['value'] if new_expense['split_method'] == 'PERCENTAGE' else None
        }
        data['expense_splits'].append(split_entry)

    save_data(data)
    return jsonify({'id': new_expense['id'], 'message': 'Expense added successfully'}), 201

@app.route('/expenses/<int:user_id>', methods=['GET'])
def get_user_expenses(user_id):
    data = load_data()
    user_expenses = [
        {**expense, 'splits': [
            split for split in data['expense_splits']
            if split['expense_id'] == expense['id'] and split['user_id'] == user_id
        ]}
        for expense in data['expenses']
        if any(split['user_id'] == user_id for split in data['expense_splits'] if split['expense_id'] == expense['id'])
    ]
    return jsonify(user_expenses), 200

@app.route('/expenses', methods=['GET'])
def get_all_expenses():
    data = load_data()
    all_expenses = [
        {**expense, 'splits': [
            split for split in data['expense_splits']
            if split['expense_id'] == expense['id']
        ]}
        for expense in data['expenses']
    ]
    return jsonify(all_expenses), 200

@app.route('/balance_sheet', methods=['GET'])
def get_balance_sheet():
    data = load_data()
    balance_sheet = []
    for user in data['users']:
        total_paid = sum(expense['amount'] for expense in data['expenses'] if expense['paid_by'] == user['id'])
        total_owed = sum(split['amount'] for split in data['expense_splits'] if split['user_id'] == user['id'])
        balance_sheet.append({
            'user_id': user['id'],
            'name': user['name'],
            'total_paid': total_paid,
            'total_owed': total_owed,
            'net_balance': total_paid - total_owed
        })
    return jsonify(balance_sheet), 200

@app.route('/balance_sheet/download', methods=['GET'])
def download_balance_sheet():
    balance_sheet = json.loads(get_balance_sheet()[0].get_data())
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['User ID', 'Name', 'Total Paid', 'Total Owed', 'Net Balance'])
    for entry in balance_sheet:
        writer.writerow([entry['user_id'], entry['name'], entry['total_paid'], entry['total_owed'], entry['net_balance']])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename=f'balance_sheet_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)