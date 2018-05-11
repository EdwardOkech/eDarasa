from django import forms

class PaymentForm(forms.Form):
    first_name = forms.CharField(label='Your First name', max_length=100)
    last_name = forms.CharField(label='Your Last name', max_length=100)
    email = forms.EmailField(label='Your Email Address', widget=forms.HiddenInput())
    description = forms.CharField(label='Payment description', max_length=200, widget=forms.HiddenInput())
    reference = forms.IntegerField(widget=forms.HiddenInput())
    amount = forms.IntegerField(widget=forms.HiddenInput())
