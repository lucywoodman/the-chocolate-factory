from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout
from django import forms

from .models import OrderDetail


class OrderDetailForm(forms.ModelForm):
    """
    Class for the order form, loaded on checkout
    """

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
        """
        Set placeholders, remove labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "sr-only"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Contact Information",
                "full_name",
                "email",
                "phone_number",
                css_class="mb-3",
            ),
            Fieldset(
                "Shipping",
                "street_address1",
                "street_address2",
                "town_or_city",
                "county",
                "postcode",
                "country",
                HTML(
                    """
                    <div class="form-check form-check-inline float-right mr-0">
                        {% if user.is_authenticated %}
                        <label for="id-save-info" class="form-check-label">Save to profile</label>
                        <input type="checkbox" name="save-info" id="id-save-info" \
                            class="form-check-input ml-2 mr-0" checked>
                        {% else %}
                        <label for="id-save-info" class="form-check-label">
                            <a href="{% url 'account_signup' %}" class="text-brand-dblue">
                                Create an account
                            </a> or
                            <a href="{% url 'account_login' %}" class="text-brand-dblue">
                                login
                            </a> to save this info.
                        </label>
                        {% endif %}
                    </div>
                    """
                ),
                css_class="mb-3",
            ),
        )

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
