from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """Set placeholders, remove labels and set autofocus on first field"""
        super().__init__(*args, **kwargs)
        placeholders = {
            "default_phone_number": "Phone number",
            "default_street_address1": "Street address 1",
            "default_street_address2": "Street address 2",
            "default_town_or_city": "Town or city",
            "default_county": "County",
            "default_postcode": "Postcode",
            "default_country": "Country",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border border-dark rounded-0"
            self.fields[field].label = False
