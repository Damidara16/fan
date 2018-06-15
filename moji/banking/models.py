from django.db import models
from django.contrib.auth.models import User
import uuid




class Wallet(models.Model):
    user = models.OneToOneField(User)
    amount = models.PositiveIntegerField(default=0)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key


'''
class TransactionHistory(models.Model):
    user = models.ForeignKey(User)
    transction =
    date =
    types = models.CharField(max_length=10, choices=Types)
'''
