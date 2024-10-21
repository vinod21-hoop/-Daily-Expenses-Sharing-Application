 Daily Expenses Sharing Application

## Overview

This Daily Expenses Sharing Application is a Flask-based web service that allows users to manage shared expenses. Users can add expenses, split them using different methods (equal, exact, or percentage), and view balance sheets.

## Features

- User Management: Create and retrieve user details
- Expense Management: Add expenses with various splitting methods
- Expense Tracking: Retrieve individual and overall expenses
- Balance Sheet: Generate and download balance sheets

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

git clone [https://github.com/yourusername/daily-expenses-sharing.git]
cd daily-expenses-sharing


2. Create a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


3. Install the required packages:

pip install -r requirements.txt

## Usage

1. Start the Flask server:


python app.py

The server will start running on `http://localhost:5000`.

2. Use the `api_client.py` script to interact with the API:


python api_client.py

This script demonstrates how to use all the API endpoints.

## API Endpoints

- `POST /users`: Create a new user
- `GET /users/<user_id>`: Retrieve user details
- `POST /expenses`: Add a new expense
- `GET /expenses/<user_id>`: Get expenses for a specific user
- `GET /expenses`: Get all expenses
- `GET /balance_sheet`: Get the current balance sheet
- `GET /balance_sheet/download`: Download the balance sheet as a CSV file

## Data Storage

The application uses a JSON file (`expenses_data.json`) to store all data. This file is created automatically when you run the application.

## Testing

To run the included tests:


python -m unittest discover tests


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
