from socket import fromshare
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

ZIP_CHOICES = (
    ('', 'Kies je gemeente'),
    ('T', '1740 - Ternat'),
    ('W', '1741 - Wambeek'),
    ('L', '1742 - Lombeek'),
    ('D', '1700 - Dilbeek'),
    ('A', '1730 - Asse'),
    ('G', '1755 - Gooik'),
)

DELIVERY_CHOICES = (
    ('P', "Haal de cocktails op bij Jurgmeister Cocktails"),
    ('D', "Laat de cocktails bij jou thuis leveren (+ € 5,00)"),
)


class CheckoutForm(forms.Form):
    delivery_method = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={
        'class': 'form-control',
    }), choices=DELIVERY_CHOICES)

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rita',
    }))

    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Peeters',
    }))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'ritapeeters@example.com',
    }))

    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '0412 34 56 78'
    }))

    street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Stationsstraat 5',
    }))

    appartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Bus 2',
    }))

    zip = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class': 'form-select',
    }), choices=ZIP_CHOICES)

    adult = forms.BooleanField(required=True)

    same_billing_address = forms.BooleanField(required=False)

    save_info = forms.BooleanField(required=False)

    def clean(self):
        data = super(CheckoutForm, self).clean()
        if data.get('delivery_method') == 'P':
            for field_name in ['street_address', 'zip']:
                if field_name in self.errors:
                    del self.errors[field_name]
    
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'Het veld {fieldname} is verplicht'.format(
                fieldname=field.label)}

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))