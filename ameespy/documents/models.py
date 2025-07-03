from django.db import models

class Document(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    fichier = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.titre
