from django import forms

class AddToOrderForm(forms.Form):
    table_uuid = forms.IntegerField(min_value=1, initial=1)
    quantity = forms.IntegerField(min_value=1, initial=1)
    price = forms.IntegerField(min_value=1, initial=1)
    product_id = forms.IntegerField(widget=forms.HiddenInput())