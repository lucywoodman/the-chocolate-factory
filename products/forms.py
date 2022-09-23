from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """
    Class for the product model form
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "producer",
            "price",
            "weight",
            "type",
            "category",
            "flavour",
            "allergy_info",
            "details",
            "ingredients",
            "image",
        ]
        widgets = {
            "type": forms.CheckboxSelectMultiple,
            "allergy_info": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        """
        Set field classes
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs[
                "class"
            ] = "border border-dark rounded-0"
