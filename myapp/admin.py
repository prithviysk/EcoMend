from django.contrib import admin
from django.utils.html import format_html

from .models import Category, PlasticListing


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image_tag']
    search_fields = ['name', 'description']
    list_filter = ['name']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        return 'No Image'

    image_tag.short_description = 'Image'


@admin.register(PlasticListing)
class PlasticListingAdmin(admin.ModelAdmin):
    list_display = ['seller', 'category', 'quantity', 'price', 'date_listed']
    search_fields = ['seller__username', 'category__name']
    list_filter = ['category', 'date_listed']
