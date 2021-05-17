from django.db import models

# Create your models here.
class Advisor(models.Model):
    name = models.CharField(max_length = 250)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name