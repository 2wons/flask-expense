# flask-expense
( python - flask - bootstrap - adminkit - postgresql )

## Preview
![image](https://github.com/2wons/flask-expense/assets/91067593/832423e1-0372-43ed-aee9-4997792e3048)

![image](https://github.com/2wons/flask-expense/assets/91067593/ecfb7416-7e79-4b77-9ff3-86fb9301a116)

![image](https://github.com/2wons/flask-expense/assets/91067593/8f62861c-60a4-4d38-978b-5482d2c4e101)

## Sprint 2 new
- added subscriptions page draft layout
## Features

* **Income and Expense Tracking:** Manage transactions (View, update ,add, delete).
* **Monthly Budgets:** Monthly categorized budgets.
* **Dashboard & statistics:** Relevant reports on transactions.
* **Multiple Accounts:**  Categorize incomes/expenses with multiple accounts.

## How to run (windows)
create venv
```
python -m venv .venv
```
activate venv
```
.\.venv\Scripts\Activate.ps1
```
install requirements
```
pip install -r requirements.txt
```

fill out .env (rename .envsample to .env)
- set up db credentials and your_secret_key

apply migrations
```
flask db upgrade
```

run
```
flask run
```
