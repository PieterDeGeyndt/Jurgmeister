from socket import fromshare
from django import forms

PAYMENT_CHOICES =(
    ('C', 'Credit Card'),
    ('D', 'Debit Card'),
)

ZIP_CHOICES=(
    ('','Choose your city'),
    ('T', '1740 - Ternat'),
    ('W', '1741 - Wambeek'),
    ('L', '1742 - Lombeek'),
    ('D', '1700 - Dilbeek'),
    ('A', '1730 - Asse'),
    ('G', '1755 - Gooik'),
)

DELIVERY_CHOICES=(
    ('P', "Pick up the cocktails at Jurgmeister's place"),
    ('D', "Get the cocktails delivered to your doorstep"),
)

class CheckoutForm(forms.Form):
    delivery_method=forms.ChoiceField(widget=forms.RadioSelect(),choices=DELIVERY_CHOICES)
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Rita',
    }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Peeters',
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ritapeeters@example.com',
    }))
    phone=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'0412 34 56 78'
    }))
    street_address=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Stationsstraat 5',
    }))
    appartment_address=forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Bus 2',
    }))
    zip=forms.ChoiceField(widget=forms.Select(attrs={
        'class':'form-select',
    }), choices=ZIP_CHOICES)
    same_billing_address=forms.BooleanField(required=False)
    save_info=forms.BooleanField(required=False)
    payment_option=forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)

