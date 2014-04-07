from django.contrib import admin

from .models import Entry, LatestEntry, Fight


class LatestEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry')


class EntryAdmin(admin.ModelAdmin):
    actions = ['force_entry_qualification']
    list_display = ('user', 'codesize', 'uploaded')

    def force_entry_qualification(self, request, queryset):
        for e in queryset:
            e.qualify()
            self.message_user(request, "qualification rescheduled for %s." % e)


class FightAdmin(admin.ModelAdmin):
    list_display = ('x', 'o', 'result', 'error')
    list_filter = ('x__user', 'o__user')


admin.site.register(Entry, EntryAdmin)
admin.site.register(LatestEntry, LatestEntryAdmin)
admin.site.register(Fight, FightAdmin)
