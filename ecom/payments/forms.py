from django import forms
from payments.models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name' }),required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address' }),required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1' }),required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2' }),required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City' }),required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State' }),required=False)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode' }),required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country' }),required=True)


    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name','shipping_email','shipping_address1' ,'shipping_address2' ,'shipping_city' ,'shipping_state' ,'shipping_zipcode' ,'shipping_country']
        exclude = ['user', ]

PAYMENT_CHOICES = [
    ('paypal', 'Paypal'),
    ('visa', 'Visa'),
    ('mastercard', 'Master Card'),
    ('discover', 'Credit Card'),
]

class PaymentForm(forms.Form):
    cardholder = forms.CharField(label="Cardholder Name",max_length=100,widget=forms.TextInput(attrs={'class': 'form-control required', 'name': 'cardholder'}))
    cardnumber = forms.CharField(label="Card Number",max_length=19,widget=forms.TextInput(attrs={'class': 'form-control required', 'name': 'cardnumber'}))
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES,widget=forms.HiddenInput(attrs={'id':'payment_type', 'name':'payment_type'}))
    mm = forms.CharField(label="MM",max_length=2,widget=forms.TextInput(attrs={'class': 'form-control required p-l-5 p-r-5 text-center', 'name': 'mm', 'placeholder': 'MM'}))
    yy = forms.CharField(label="YY",max_length=2,widget=forms.TextInput(attrs={'class': 'form-control required p-l-5 p-r-5 text-center','name': 'yy', 'placeholder': 'YY'}))
    cvv = forms.CharField(label="CVV",max_length=4,widget=forms.TextInput(attrs={'class': 'form-control required p-l-5 p-r-5 text-center','name':'cvv'}))

