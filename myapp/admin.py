from django.contrib import admin
from .models import *

class HistoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'search_query', 'selected_disk', 'timestamp', 'file_extension', 'result']
	search_fields = ['search_query']
	list_filter = ['selected_disk']
	date_hierarchy = 'timestamp'
	list_per_page = 10
admin.site.register(History, HistoryAdmin)

class LogAdmin(admin.ModelAdmin):
	list_display = ['id', 'search_query', 'selected_disk', 'timestamp', 'file_extension']
	search_fields = ['search_query']
	list_filter = ['selected_disk']
	date_hierarchy = 'timestamp'
	list_per_page = 10
admin.site.register(Log, LogAdmin)

admin.site.site_header = "SEH"

admin.site.register(AuthToken)
