from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    video = models.FileField(upload_to='events/videos/', blank=True, null=True)

    def __str__(self):
        return self.title


