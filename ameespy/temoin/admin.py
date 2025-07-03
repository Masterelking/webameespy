from django.contrib import admin
from .models import Temoignage

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'message')  # Affichage en liste
    search_fields = ('nom',)  # Ajout d’un champ de recherche
