from django import forms

class DonationForm(forms.Form):
    quantity = forms.DecimalField(min_value=0.01, required=True, label="Donation Quantity", help_text="In USD")
