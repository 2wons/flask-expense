from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length
from decimal import Decimal
from datetime import datetime ,date

class RecordForm(FlaskForm, object):

    name = StringField('Name', 
                       validators=[DataRequired(), Length(min=1, max=64)])
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

    def fill_from_record(self, record):
        self.name.data = record.name
        self.amount.data = record.amount
        self.category.data = record.category
        self.date_spent.data = record.date
        self.note.data = record.note
        self.account.data = record.account_id

class AccountForm(FlaskForm):

    name = StringField('Name',
                       validators=[DataRequired(), Length(min=1, max=64)])
    group = SelectField('Group',
                        validators=[DataRequired()],
                        choices=[("Cash", "Cash"), ("Bank", "Bank"), ("Card", "Card")])
    
    # initial balance
    # description

    submit = SubmitField('Add Account')
    