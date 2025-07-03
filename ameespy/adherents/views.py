from django.shortcuts import render, redirect
from .forms import AdherentForm
from .models import Adherent

def adherer(request):
    error_message = None  # Ajout d'un message d'erreur en cas de doublon
    
    if request.method == "POST":
        form = AdherentForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            contact = form.cleaned_data['contact']
            
            # Vérification si l'adhérent existe déjà
            if Adherent.objects.filter(nom=nom, contact=contact).exists():
                error_message = "⚠️ Cet adhérent existe déjà."
            else:
                form.save()
                return redirect('adherer_success')
    
    else:
        form = AdherentForm()
    
    return render(request, 'adherents/adherer.html', {'form': form, 'error_message': error_message})

def adherer_success(request):
    return render(request, 'adherents/adherer_success.html')
