from django.contrib import admin
from .models import Category, Flavour, Allergy, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("nice_name", "name")


class FlavourAdmin(admin.ModelAdmin):
    list_display = ("nice_name", "name")


class AllergyAdmin(admin.ModelAdmin):
    list_display = ("nice_name", "name")


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "weight",
        "image",
    )

    ordering = ("sku",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Flavour, FlavourAdmin)
admin.site.register(Allergy, AllergyAdmin)
admin.site.register(Product, ProductAdmin)
