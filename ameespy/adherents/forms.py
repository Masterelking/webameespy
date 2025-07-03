from django import forms
from .models import Adherent

class AdherentForm(forms.ModelForm):
    class Meta:
        model = Adherent
        fields = ['nom', 'prenoms', 'adresse', 'contact', 'niveau_etude', 'sexe']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'village,quartier'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telephone'}),
            'niveau_etude': forms.Select(attrs={'class': 'form-select'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
        }
