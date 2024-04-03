# flask-expense
( python - flask - bootstrap - adminkit - postgresql )

## Preview
![image](https://github.com/2wons/flask-expense/assets/91067593/832423e1-0372-43ed-aee9-4997792e3048)

![image](https://github.com/2wons/flask-expense/assets/91067593/ecfb7416-7e79-4b77-9ff3-86fb9301a116)

![image](https://github.com/2wons/flask-expense/assets/91067593/8f62861c-60a4-4d38-978b-5482d2c4e101)

![image](https://github.com/2wons/flask-expense/assets/91067593/411d5334-2d9e-4cea-811d-e05ccac7a5f1)

  
## Features

* **Income and Expense Tracking:** Manage transactions (View, update ,add, delete).
* **Monthly Budgets:** Monthly categorized budgets.
* **Dashboard & statistics:** Relevant reports on transactions.
* **Multiple Accounts:**  Categorize incomes/expenses with multiple accounts.
* **Subsciptions Tracking:**  Track recurring payments

## How to run (windows)
create venv
```
python -m venv .venv
```
activate venv
```ps
# windows
.\.venv\Scripts\Activate.ps1
```
```bash
# unix/mac
source .venv/bin/activate
```
install requirements
```
pip install -r requirements.txt
```

fill out .env (rename .envsample to .env)
- set up db credentials and your_secret_key
- to use sqlite, leave db credentials blank

Example .env
```env
FLASK_APP=run.py
FLASK_DEBUG=1

# secret-key
SECRET_KEY=75376d35f1b0ad433908bb5a4b5c9b9a
# Db credentials can be blank to run sqlite
```

apply migrations (needed to create db)
```
flask db upgrade
```

run
```
flask run
```
