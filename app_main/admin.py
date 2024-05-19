from django.contrib import admin

from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created', 'updated')
    list_display_links = ('title',)
    search_fields = ('title', 'owner', 'body')
    list_filter = ('created', 'updated')
    ordering = ('title', 'owner')
    