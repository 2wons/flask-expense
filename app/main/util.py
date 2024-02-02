from flask_login import current_user

def get_categories(cat_type:str):

    categories = None
    if cat_type == 'expense':
        categories = [
            'Food',
            'Grocery',
            'Medical',
            'Bills',
            'Entertainment',
            'Shopping',
            'Travel',
            'Debt',
            'Loan',
            'Other'
        ]
    elif cat_type == 'income':
        categories = [
            'Allowance',
            'Salary',
            'Passive',
            'Bonus',
            'Gift',
            'Investment',
            'Tips',
            'Other'
    ]

    return [(category, category) for category in categories]

def get_accounts():

    accounts = [(account.id, account.name) for account in current_user.accounts]
    return accounts