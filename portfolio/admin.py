from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Project, Image, Comment

# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'demo_url', 'direction',
                    'sequence_number', 'get_add_date')
    list_filter = ('direction', )
    search_fields = ('name', 'demo_url', 'short_description')

    inlines = (ImageInline,)
    ordering = ('sequence_number',)

    def get_add_date(self, obj):
        return obj.create_at.strftime("%d/%m/%Y")
    get_add_date.short_description = "Add Date"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'view_image')

    def view_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" style="border-radius:10%;" />')
    view_image.short_description = 'Rasm'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'project', 'status', 'get_date')
    ordering = ('-create_at',)
    list_filter = ('status',)
    list_editable = ('status',)
