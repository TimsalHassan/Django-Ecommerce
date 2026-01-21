from django import forms
from payments.models import ShippingAddressFormModel

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddressFormModel
        fields = ['first_name', 'last_name', 'email', 'company_name', 'area_code', 'primary_phone', 'address_1', 'address_2','city', 'state', 'zip_code', 'country', 'business_address',]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',  
            'company_name': 'Company Name (optional)',
            'area_code': 'Area Code',
            'primary_phone': 'Primary Phone',
            'address_1': 'Street Address',
            'city': 'City',
            'state': 'State/Province',
            'zip_code': 'ZIP Code',
            'country': 'Country',
            'business_address': 'This is a business address',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'area_code': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_1': forms.TextInput(attrs={'class': 'form-control m-b-10'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control'}),
            'address_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address': forms.CheckboxInput(attrs={'class': ''}),
        }



