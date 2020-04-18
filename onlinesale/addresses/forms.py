from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_to_name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'pin_code'
        ]

# widget defines how the field box should look
# here we have defined a class for every fields widget
        widgets = {

            'address_to_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.NumberInput(attrs={'class': 'form-control'}),
        }