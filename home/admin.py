from django.contrib import admin

from home.models import Product, Producer


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "producer", "price", "category", "year"]
    list_display_links = ["producer", "category"]
    list_filter = ["producer", "category"]
    search_fields = ["name", "price"]
    list_editable = ["name", "year"]
    fieldsets = [
        (
            None,
            {"fields": ("name",)}
        ),
        (
            "Product type",
            {"fields": ("category",)}
        ),
        (
            "Product info",
            {"fields": ("producer", "price", "year", "description")}
        ),
        (
            "image",
            {"fields": ("image",)}
        )
    ]

    def get_search_results(self, request, queryset, search_term):
        if search_term.isdigit():
            return queryset.filter(price__gte=search_term), False
        return super().get_search_results(request, queryset, search_term)


admin.site.register(Product, ProductAdmin)
