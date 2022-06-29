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
        
        
class Nbasket(models.Model):
    gr = models.IntegerField(blank=True, null=True)
    pname = models.CharField(max_length=150, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nbasket'


class Tbasket(models.Model):
    b_num = models.IntegerField(blank=True, null=True)
    b_pname = models.CharField(max_length=150, blank=True, null=True)
    b_price = models.IntegerField(blank=True, null=True)
    g_pname = models.CharField(max_length=150, blank=True, null=True)
    g_price = models.IntegerField(blank=True, null=True)
    f_pname = models.CharField(max_length=150, blank=True, null=True)
    f_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbasket'