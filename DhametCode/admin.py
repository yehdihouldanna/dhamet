from django.contrib import admin
from .models import Game, Player
# Register your models here.

# in order to have the data bases appear as tables in the admin page:
class GameAdmin(admin.ModelAdmin):
    list_display = ("DateTime","Length","Winner")

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("Name",)

admin.site.register(Game,GameAdmin)
admin.site.register(Player,PlayerAdmin)