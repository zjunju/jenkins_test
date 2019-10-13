from django.contrib import admin

from .models import Site, SiteHistory


class SiteModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'href', 'coding', 'need_verification', ]
    search_fields = ['name']


class SiteHistoryAdmin(admin.ModelAdmin):
    # list_display_links = ['site']
    list_display = ['site', 'verification_date', 'result', 'certificate', 'site_type']
    list_filter = ['site_type']


admin.site.register(Site, SiteModelAdmin)
admin.site.register(SiteHistory, SiteHistoryAdmin)
