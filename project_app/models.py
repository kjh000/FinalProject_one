from django.db import models

class Basket(models.Model):
    pname = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'basket'

class Fbasket(models.Model):
    pname = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fbasket'


class Gbasket(models.Model):
    pname = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gbasket'