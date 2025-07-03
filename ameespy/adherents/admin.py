from django.contrib import admin
from .models import Adherent

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'niveau_etude', 'sexe')  # Personnalisation de l'affichage
    search_fields = ('nom', 'prenoms')  # Ajout d'un champ de recherche
