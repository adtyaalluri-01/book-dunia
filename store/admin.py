from django.contrib import admin
from django.utils.html import format_html
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'rating', 'category', 'cover_preview']
    list_display_links = ['title']
    search_fields = ['title', 'category']
    list_filter = ['category']
    readonly_fields = ['cover_preview']

    def cover_preview(self, obj):
        if obj.cover and hasattr(obj.cover, 'url'):
            return format_html("<img src='{}' style='max-height: 200px;' />", obj.cover.url)
        return format_html("<span style='color: #999;'>No image</span>")

    cover_preview.short_description = "Cover Preview"