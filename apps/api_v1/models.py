from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    logo_img_path = models.CharField(max_length=100)
    restaurant_img_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name
