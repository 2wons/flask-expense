from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, DateField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from app.models import Record

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
    type = HiddenField('Type',
                       validators=[Optional()])
    prev_url = HiddenField('Prev URL',
                            validators=[Optional()])
    submit = SubmitField('Add')

    def validate_amount(self, amount):
        if amount.data == 0:
            raise ValidationError('Amount must not be 0.')
        if amount.data < 0:
            raise ValidationError('Amount must be greater than 0.')

    def fill_from_record(self, record):
        self.name.data = record.name
        self.amount.data = abs(record.amount)
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

    submit = SubmitField('Add Account')

class ResetForm(FlaskForm):

    old_password = PasswordField('Old Password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired()])
    confirm_new = PasswordField('Confirm new Password',
                             validators=[DataRequired(), EqualTo('new_password')])
    
    submit = SubmitField('Reset Password')
    
    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Invalid old password')

def create_record(form):
    type = form.type.data
    if type == 'expense':
        amount = -form.amount.data
    else:
        amount = form.amount.data
    record = Record(
            name        =form.name.data,
            amount      =amount,
            date        =form.date_spent.data,
            account_id  =form.account.data,
            category    =form.category.data,
            note        =form.note.data,
            type        =type
        )
    return record