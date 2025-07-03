from django.db import models

class Adherent(models.Model):
    nom = models.CharField(max_length=100  )
    prenoms = models.CharField(max_length=150 )
    adresse = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    niveau_etude = models.CharField(
        max_length=50,
        choices=[
            ('Collège', 'Collège'),
            ('Lycée', 'Lycée'),
            ('Licence', 'Licence'),
            ('Master', 'Master'),
            ('Doctorat', 'Doctorat')
        ]
    )
    sexe = models.CharField(
        max_length=10,
        choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')]
    )

    def __str__(self):
        return f"{self.nom} {self.prenoms} ({self.niveau_etude})"
