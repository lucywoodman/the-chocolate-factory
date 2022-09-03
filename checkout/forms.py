from django import forms
from .models import OrderDetail


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = (
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "town_or_city",
            "county",
            "postcode",
            "country",
        )

    def __init__(self, *args, **kwargs):
        """Set placeholders, remove labels and set autofocus on first field"""
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full name",
            "email": "Email address",
            "phone_number": "Phone number",
            "street_address1": "Street address 1",
            "street_address2": "Street address 2",
            "town_or_city": "Town or city",
            "county": "County",
            "postcode": "Postcode",
            "country": "Country",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"
            self.fields[field].label = False
