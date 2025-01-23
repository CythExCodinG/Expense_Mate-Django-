from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
  user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
  description = models.CharField(max_length=100)
  category = models.CharField(max_length=50, default='other')
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateField(default=now)
  
class Budget(models.Model):
  user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  # date = models.DateField(default=now)

class Recurringexpense(models.Model):
  user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
  description = models.CharField(max_length=100)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateField(default=now)
  