from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Tour, Category


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_foto', 'cat','tags']
    #filter_horizontal = ['tags']
    readonly_fields = ['post_foto']
    prepopulated_fields = {"slug": ("title", )}
    filter_vertical = ['tags']
    list_display = ('title', 'post_foto', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True
    
    @admin.display(description="Фото", ordering='content')
    def post_foto(self, tour: Tour):
        if tour.photo:
            return mark_safe(f"<img src='{tour.photo.url}' width=50>")
        return "Без фото"
    
    @admin.action(description="Опубликовать выбранные турниры")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Tour.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} турниров.")
        
    @admin.action(description="Снять с публикации выбранные турниры")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Tour.Status.DRAFT)
        self.message_user(request, f"{count} турниров сняты с публикации.", messages.WARNING)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
