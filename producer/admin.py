from django.contrib import admin

from producer.models import Producer


class ProducerAdmin(admin.ModelAdmin):
    list_display = ["producer_name"]
    list_filter = ["categories"]
    search_fields = ["producer_name"]
    fieldsets = [
        (
            None,
            {"fields": ("producer_name",)}
        ),
        (
            "Producer info",
            {"fields": ("categories", "description")}
        ),
        (
            "image",
            {"fields": ("logo",)}
        )
    ]


admin.site.register(Producer, ProducerAdmin)
