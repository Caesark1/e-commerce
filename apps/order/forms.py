from django import forms


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    appartment_address = forms.CharField(required = False)