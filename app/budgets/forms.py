from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, date
from app.models import Budget


class BudgetForm(FlaskForm):

    # Generate months dynamically
    months = [(str(month), datetime(1900, month, 1).strftime('%B'))
              for month in range(1, 13)]

    # Generate years dynamically from the current year to current year + 5 more years
    current_year = datetime.now().year
    years = [(str(year), str(year))
             for year in range(current_year, current_year + 6)]

    month = SelectField('Month', choices=months, validators=[DataRequired()])
    year = SelectField('Year', choices=years, validators=[DataRequired()])

    submit = SubmitField('Create')

    # Define a DecimalField for each category with a default value of 0
    food_limit = DecimalField('Food_limit', default=0,
                              validators=[Optional()])
    grocery_limit = DecimalField(
        'Grocery_limit', default=0, validators=[Optional()])
    medical_limit = DecimalField(
        'Medical_limit', default=0, validators=[Optional()])
    bills_limit = DecimalField(
        'Bills_limit', default=0, validators=[Optional()])
    entertainment_limit = DecimalField(
        'Entertainment_limit', default=0, validators=[Optional()])
    shopping_limit = DecimalField(
        'Shopping_limit', default=0, validators=[Optional()])
    travel_limit = DecimalField(
        'Travel_limit', default=0, validators=[Optional()])
    debt_limit = DecimalField('Debt_limit', default=0,
                              validators=[Optional()])
    loan_limit = DecimalField('Loan_limit', default=0,
                              validators=[Optional()])
    other_limit = DecimalField(
        'Other_limit', default=0, validators=[Optional()])

    def limits_to_dict(self):
        """Serializes category limits data to json/dict"""
        limits = {}
        for field_name, field in self._fields.items():
            if field_name.endswith('_limit'):
                # Strip '_limit' from the field name to get the category name
                category_name = field_name.replace('_limit', '')
                # Use the field's data for the value, defaulting to 0 if it's None
                limits[category_name] = float(field.data if field.data is not None else 0)
        return limits
    
    def limit_sum(self):
        """Returns the sum of all limits."""
        total_sum = 0
        for field_name, field in self._fields.items():
            if field_name.endswith('_limit'):
                # Add the field's data to the total sum. The data will be `0` by default if not entered.
                total_sum += field.data if field.data is not None else 0
        return total_sum
    
    def fill_from_budget(self, budget: Budget):
        """Fills the form with the given budget's data"""
        self.month.data = str(budget.month)
        self.year.data = str(budget.year)
        self.food_limit.data = budget.limits_dict.get('food', 0)
        self.grocery_limit.data = budget.limits_dict.get('grocery', 0)
        self.medical_limit.data = budget.limits_dict.get('medical', 0)
        self.bills_limit.data = budget.limits_dict.get('bills', 0)
        self.entertainment_limit.data = budget.limits_dict.get('entertainment', 0)
        self.shopping_limit.data = budget.limits_dict.get('shopping', 0)
        self.travel_limit.data = budget.limits_dict.get('travel', 0)
        self.debt_limit.data = budget.limits_dict.get('debt', 0)
        self.loan_limit.data = budget.limits_dict.get('loan', 0)
        self.other_limit.data = budget.limits_dict.get('other', 0)
        
