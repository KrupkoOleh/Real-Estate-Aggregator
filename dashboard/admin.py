from django.contrib import admin

from dashboard.models import Listening, Image


class ListeningImageAttributeInline(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Listening)
class ListeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'link')
    inlines = [ListeningImageAttributeInline]
