from django.contrib import admin
from . import models

class DisplayData(admin.ModelAdmin):
	list_display = ['username', 'id', 'verified', 'about', 'answers', 'web_site', 'commented', 'reputation']


admin.site.register(models.User_data, DisplayData)
