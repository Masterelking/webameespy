from django.db import models

class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='temoignage_images/', blank=True, null=True)

    def __str__(self):
        return self.nom
