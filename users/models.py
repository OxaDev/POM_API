from django.db import models
from datetime import date

class User(models.Model):
  username = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  joined_date = models.CharField(max_length=255,null=True)

  def __str__(self):
    return f"{self.username} {self.email}"

