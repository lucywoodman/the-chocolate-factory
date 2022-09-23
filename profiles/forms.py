from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    """
    Class for user model form
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        """
        Set placeholders, remove labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email address",
        }

        self.fields["first_name"].widget.attrs["autofocus"] = True
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


class ProfileForm(forms.ModelForm):
    """
    Class for profile model form
    """

    class Meta:
        model = Profile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Set placeholders and remove labels
        """
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
