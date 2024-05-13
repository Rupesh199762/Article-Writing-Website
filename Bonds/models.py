from django.db import models

class BondModel(models.Model):
    bond_id = models.CharField(max_length=100,primary_key=True)
    date_of_purchase = models.DateField()
    name_of_purchaser = models.TextField()
    date_of_expiry = models.DateField()
    name_of_political_party = models.TextField()
    date_of_encashment = models.DateField()
    denomination = models.IntegerField()
    status = models.CharField(max_length=50)
    short_name = models.CharField(null=True, max_length=15)




# Create your models here.
