from django.db import models

class Test(models.Model):
    image = models.ImageField(upload_to='img/')
