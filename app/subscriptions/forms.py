from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, DateField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Subscription

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
                          coerce=int,
                            validators=[DataRequired()])
    
    # status radio
    status = RadioField('Status',
                        choices=[('active', 'Active'), ('cancelled', 'Cancelled')],
                        default='active')
    
    submit = SubmitField('Add Subscription')

    def validate_price(self, price):
        if price.data < 0:
            raise ValidationError('Price must be greater than 0.')
    
    def fill_from_model(self, subscription):
        self.provider.data   = subscription.provider
        self.price.data      = subscription.price
        self.billing.data    = subscription.billing
        self.start_date.data = subscription.start_date
        self.category.data   = subscription.category
        self.account.data    = subscription.account_id
        self.status.data     = subscription.status

def create_subscription(form):

    subscription = Subscription(
        provider   =   form.provider.data,
        price      =   form.price.data,
        billing    =   form.billing.data,
        start_date =   form.start_date.data,
        category   =   form.category.data,
        account_id =   form.account.data,
        status     =   'active'
    )
    return subscription

def update_subscription(subscription, form):

    subscription.provider   = form.provider.data
    subscription.price      = form.price.data
    subscription.billing    = form.billing.data
    subscription.start_date = form.start_date.data
    subscription.category   = form.category.data
    subscription.account_id = form.account.data
    subscription.status     = form.status.data

    return subscription