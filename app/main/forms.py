from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length


class ExpenseForm(FlaskForm):

    name = StringField('Name', 
                       validators=[DataRequired()])
    amount = DecimalField('Amount',
                          validators=[DataRequired()])
    date_spent = DateField('Date Spent',
                           validators=[DataRequired()])
    account = SelectField('Account', coerce=int,
                           validators=[DataRequired()])
    category = SelectField('Category',
                           validators=[DataRequired()])
    note = TextAreaField('Note',
                         validators=[Length(max=60)])
    submit = SubmitField('Add')

class AccountForm(FlaskForm):

    name = StringField('Name',
                       validators=[DataRequired()])
    group = SelectField('Group',
                        validators=[DataRequired()],
                        choices=[("Cash", "Cash"), ("Bank", "Bank"), ("Card", "Card")])
    submit = SubmitField('Add Account')
    