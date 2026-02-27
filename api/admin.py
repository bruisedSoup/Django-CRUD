from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'year', 'genre', 'isbn', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('genre',)
    readonly_fields = ('created_at', 'updated_at')