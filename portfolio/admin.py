from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Project, Image

# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'demo_url', 'direction', 'get_add_date')
    list_filter = ('direction', )
    search_fields = ('name', 'demo_url', 'short_description')

    inlines = (ImageInline,)

    def get_add_date(self, obj):
        return obj.create_at.strftime("%d/%m/%Y")
    get_add_date.short_description = "Add Date"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'view_image')

    def view_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" style="border-radius:10%;" />')
    view_image.short_description = 'Rasm'
