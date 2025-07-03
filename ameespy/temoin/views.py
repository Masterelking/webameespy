from django.shortcuts import render
from .models import Temoignage

def temoignage_list(request):
    temoignages = Temoignage.objects.all()  # Récupérer tous les témoignages
    return render(request, 'temoin/temoin.html', {'temoignages': temoignages})
