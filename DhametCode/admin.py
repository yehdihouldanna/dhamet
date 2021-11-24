from django.contrib import admin
from .models import Game
# Register your models here.

# in order to have the data bases appear as tables in the admin page:
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk','created','completed','creator','opponent','state','length','moves')

admin.site.register(Game,GameAdmin)