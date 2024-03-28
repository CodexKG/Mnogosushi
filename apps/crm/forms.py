from django import forms
from apps.billing.models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'  # Или перечислите поля, которые хотите включить в форму