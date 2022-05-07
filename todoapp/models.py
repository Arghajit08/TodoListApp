from django.db import models

class Todo(models.Model):
    id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

# Create your models here.
