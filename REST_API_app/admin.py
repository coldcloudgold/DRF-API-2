from django.contrib import admin

from .models import Handbook, ItemHandbook


class HandbookAdmin(admin.ModelAdmin):
    list_display = ("global_id", "name", "version","validity_date")
    search_fields = ("global_id",)
    empty_value_display = "-пусто-"


class ItemHandbookAdmin(admin.ModelAdmin):
    list_display = ("handbook", "code", "value")
    search_fields = ("code", "value")
    empty_value_display = "-пусто-"


admin.site.register(Handbook, HandbookAdmin)
admin.site.register(ItemHandbook, ItemHandbookAdmin)
