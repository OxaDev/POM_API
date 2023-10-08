from django.db import models
from datetime import date

class User(models.Model):
  username = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  joined_date = models.DateField(null=True)

  def __str__(self):
    return f"{self.username} {self.email}"

class Token(models.Model):
  token_value = models.CharField(max_length=512)
  creation_date = models.CharField(max_length=512,null= True)
  delete_date = models.CharField(max_length=512,null= True) 
  email_user = models.CharField(max_length=255,null= True)

  def __str__(self):
    return f"Token : {self.token_value} --- Expire Date : {self.delete_date} --- Assigned to : {self.email_user}"