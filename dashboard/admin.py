from django.contrib import admin

from dashboard.models import Listening


@admin.register(Listening)
class ListeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'link')
