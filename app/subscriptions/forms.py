from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, DateField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional

class SubscriptionForm(FlaskForm):

    provider = StringField('Provider',
                            validators=[DataRequired(), Length(min=1, max=64)])
    price = DecimalField('Price', 
                            validators=[DataRequired()])
    billing = SelectField('Billing',
                            validators=[DataRequired()],
                            choices=[("Monthly", "Monthly"), ("Yearly", "Yearly")])

    # start_date
    start_date = DateField('Start Date',
                            validators=[DataRequired()])
    # category
    category = SelectField('Category',
                            validators=[DataRequired()])
    # account
    account = SelectField('Account',
                            validators=[DataRequired()])
    submit = SubmitField('Add Subscription')