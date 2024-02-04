from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired
from datetime import datetime ,date
from app.main.util import get_categories

class BudgetForm(FlaskForm):

     # Generate months dynamically
    months = [(str(month), datetime(1900, month, 1).strftime('%B')) for month in range(1, 13)]

    # Generate years dynamically from the current year to current year + 5 more years
    current_year = datetime.now().year
    years = [(str(year), str(year)) for year in range(current_year, current_year + 6)]

    month = SelectField('Month', choices=months, validators=[DataRequired()])
    year = SelectField('Year', choices=years, validators=[DataRequired()])

    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)

        # Create DecimalFields dynamically based on the list of categories
        for category in get_categories("expense"):
            field_name = f"{category}_limit"
            setattr(self, field_name, DecimalField(category, validators=[DataRequired()]))

    def limits_to_dict(self):
        """serializes category limits data to json/dict"""
        pass
    
    