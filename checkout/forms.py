from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    Layout,
    Fieldset,
    Div,
    HTML,
    ButtonHolder,
)
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
        self.helper.form_id = "payment-form"
        self.helper.label_class = "sr-only"
        self.helper.form_method = "POST"
        self.helper.form_action = "checkout"
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
                    """<div class="form-check form-check-inline float-right mr-0">
                        <!-- If customer is logged in, allow them to save details to their profile -->
                        {% if user.is_authenticated %}
                            <label for="id-save-info" class="form-check-label">Save to profile</label>
                            <input type="checkbox" name="save-info" id="id-save-info" class="form-check-input ml-2 mr-0" checked>
                        <!-- Else offer them the option to register or login -->
                        {% else %}
                            <label for="id-save-info" class="form-check-label">
                                <a href="{% url 'account_signup' %}" class="text-info">Create an account</a> or
                                <a href="{% url 'account_login' %}" class="text-info">login</a> to save this info.
                            </label>
                        {% endif %}
                    </div>"""
                ),
            ),
            Fieldset(
                "Payment",
                Div(
                    css_id="card-element",
                    css_class="mb-3",
                ),
                Div(
                    css_id="card-errors",
                    css_class="mb-3 text-danger",
                    role="alert",
                ),
                HTML(
                    """<input type="hidden" value="{{ client_secret }}" name="client_secret">"""
                ),
            ),
            Div(
                Div(
                    HTML(
                        """<a href="{% url 'view_bag' %}" class="btn btn-brand-pink rounded-0 py-2 theme-btn"><i class="icon fa-solid fa-arrow-left px-1" aria-hidden="true"></i> Return to Bag</a>"""
                    ),
                    HTML(
                        """<button id="submit-button" class="btn btn-primary rounded-0 py-2 theme-btn"><i class="icon fa-solid fa-lock px-1" aria-hidden="true"></i> Pay Now <i class="icon fa-solid fa-arrow-right px-1" aria-hidden="true"></i></button>"""
                    ),
                    css_class="d-flex align-items-start justify-content-between",
                ),
                HTML(
                    """<p class="small mt-2 text-danger text-end">Your card will be charged £{{ grand_total|floatformat:2 }}</p>"""
                ),
                css_class="mt-5 mb-2",
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
