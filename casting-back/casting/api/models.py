from django.db import models

# Create your models here.


class Castings(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    photo = models.TextField()

def __str__(self) -> str:
    return self.name

def to_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'photo': self.photo
    }

