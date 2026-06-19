from django.contrib import admin

from .models import Event, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "sku", "created_at")
    list_filter = ("category",)
    search_fields = ("name", "category", "sku")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "location", "event_date", "max_guests", "created_at")
    list_filter = ("event_date", "location")
    search_fields = ("title", "location")
