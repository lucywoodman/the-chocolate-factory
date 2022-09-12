from django.contrib import admin
from .models import Category, Flavour, Allergy, Product, Type


class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

    ordering = ("name",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class FlavourAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class AllergyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "weight",
        "image",
    )

    ordering = ("name",)


admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Flavour, FlavourAdmin)
admin.site.register(Allergy, AllergyAdmin)
admin.site.register(Product, ProductAdmin)
