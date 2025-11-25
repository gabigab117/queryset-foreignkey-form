from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Animal(models.Model):
    breed = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    veterinarian = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} chien de {self.owner.username}"

class Appointment(models.Model):
    date = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"RDV for {self.animal.name} on {self.date}"