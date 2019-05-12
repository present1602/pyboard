from django import forms


class AddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.HiddenInput)
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

