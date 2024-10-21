import requests
import json

BASE_URL = "http://localhost:5000"

def create_user(name, email, mobile):
    url = f"{BASE_URL}/users"
    data = {
        "name": name,
        "email": email,
        "mobile": mobile
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def add_expense(description, amount, paid_by, split_method, splits):
    url = f"{BASE_URL}/expenses"
    data = {
        "description": description,
        "amount": amount,
        "paid_by": paid_by,
        "split_method": split_method,
        "splits": splits
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_user_expenses(user_id):
    url = f"{BASE_URL}/expenses/{user_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_all_expenses():
    url = f"{BASE_URL}/expenses"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_balance_sheet():
    url = f"{BASE_URL}/balance_sheet"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def download_balance_sheet():
    url = f"{BASE_URL}/balance_sheet/download"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('balance_sheet.csv', 'wb') as f:
            f.write(response.content)
        print("Balance sheet downloaded as 'balance_sheet.csv'")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Test the functionality
if __name__ == "__main__":
    # Create users
    user1 = create_user("Alice", "alice@example.com", "1234567890")
    user2 = create_user("Bob", "bob@example.com", "0987654321")
    user3 = create_user("Charlie", "charlie@example.com", "1122334455")

    if user1 and user2 and user3:
        print("Users created successfully")
        print(f"User1: {json.dumps(user1, indent=2)}")
        print(f"User2: {json.dumps(user2, indent=2)}")
        print(f"User3: {json.dumps(user3, indent=2)}")
        
        # Add expenses
        expense1 = add_expense("Dinner", 100, user1['id'], "EQUAL", [
            {"user_id": user1['id'], "value": 0},
            {"user_id": user2['id'], "value": 0},
            {"user_id": user3['id'], "value": 0}
        ])
        
        expense2 = add_expense("Movie", 60, user2['id'], "EXACT", [
            {"user_id": user1['id'], "value": 20},
            {"user_id": user2['id'], "value": 20},
            {"user_id": user3['id'], "value": 20}
        ])
        
        expense3 = add_expense("Groceries", 150, user3['id'], "PERCENTAGE", [
            {"user_id": user1['id'], "value": 30},
            {"user_id": user2['id'], "value": 30},
            {"user_id": user3['id'], "value": 40}
        ])
        
        if expense1 and expense2 and expense3:
            print("Expenses added successfully")
            print(f"Expense1: {json.dumps(expense1, indent=2)}")
            print(f"Expense2: {json.dumps(expense2, indent=2)}")
            print(f"Expense3: {json.dumps(expense3, indent=2)}")
            
            # Get user expenses
            alice_expenses = get_user_expenses(user1['id'])
            print(f"Alice's expenses: {json.dumps(alice_expenses, indent=2)}")
            
            # Get all expenses
            all_expenses = get_all_expenses()
            print(f"All expenses: {json.dumps(all_expenses, indent=2)}")
            
            # Get balance sheet
            balance_sheet = get_balance_sheet()
            print(f"Balance sheet: {json.dumps(balance_sheet, indent=2)}")
            
            # Download balance sheet
            download_balance_sheet()
        else:
            print("Failed to add expenses")
    else:
        print("Failed to create users")