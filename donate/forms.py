from django import forms

class DonationForm(forms.Form):
    METHOD_DWOLLA = 0
    METHOD_STRIPE = 1
    METHODS = (
      (METHOD_DWOLLA, 'Dwolla'),
      (METHOD_STRIPE, 'Credit Card via Stripe')
    )
    method = forms.ChoiceField(choices=METHODS)
    quantity = forms.DecimalField(min_value=0.5, required=True, label="Donation Quantity", help_text="In USD")

class StripeForm(forms.Form):
    MONTHS = map(lambda x:(x, x), range(1, 13))
    YEARS = map(lambda x:(x, x), range(2012, 2026))
    card = forms.CharField(label="Card Number")
    month = forms.ChoiceField(choices=MONTHS, label='Expiration Month')
    year = forms.ChoiceField(choices=YEARS, label='Expiration Year')
    cvc = forms.IntegerField(label='CVC', help_text='Three digits found on back of card')
