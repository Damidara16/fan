from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import stripe

class Product(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=80, default='')

    def save(self, *args, **kwargs):
        self.name = self.user.username + ' FanMoji Account '
        return super(Product, self).save(*args, **kwargs)

    def StripeProductCall(self):
    #need to create secret key in settings that imports
    #change stripe key in settings to account passcode
        stripe.api_key = settings.STRIPE_KEY

        a = stripe.Product.create(
          name= self.name + 'subscription plan',
          type='service',
        )
        self.stripe_id = a['id']
        self.save()

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255)
    nickname = models.CharField(max_length=105)
    stripe_id = models.CharField(max_length=80, default='')

#make sure price matches with django numbers
    def StripePlanCall(self):
        a = stripe.Plan.create(
          nickname=self.nickname,
          product=self.user.product.stripe_id,
          amount= self.price,
          currency="usd",
          interval="month",
        )
        self.stripe_id = a['id']
        self.save()

'''
def MakePlan(sender, **kwargs):
    if kwargs['created']:
        #make api call to stripe and make actual plan
        pass

post_save.connect(MakePlan, sender=Plan)
'''

class Points(models.Model):
    #each user is assigned a point model
    #and when a fan does an action, a view will reference the celeb point model add that value
    #based on the model.
    #points are added to a fan-celeb 'bank account' which can only be access by the fan
    user = models.OneToOneField(User)
    likes = models.PositiveIntegerField(default=0)
    comment = models.PositiveIntegerField(default=0)
    #have a view that adds and subtrack points based on the operation
    def __str__(self):
        return self.user.username

class PointsWallet(models.Model):
    #add a post save signal that creates a pointswallet when users add each other
    walletname = models.CharField(max_length=115)
    user = models.ForeignKey(User)
    amount = models.PositiveIntegerField(default=0)
    #uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username + ' Points Wallet with ' + self.walletname

class Tip(models.Model):
    tipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Donor')
    tipped = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Donated')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    reason = models.CharField(max_length=255)

'''
class Reward(models.Model):
    #so celeb sets reward, fan claims reward,
    #1.points are reduced, 2.email sent to celeb and fan, 3.if reward is any of the choice. Our system will automatically do the action
    #4.if it is custom then the celeb will sent the email saying to follow through on the reward and our system will track the process
    Prizes = (('discount','D'), ('first access', 'FA'), ('real item', 'RI'), ('custom', 'C'))
    cost = models.PositiveIntegerField(default=0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #remdeemer = models.ForeignKey(User)
    prize = models.CharField(max_length=10, choices=Prizes)
    description = models.CharField(max_length=255)
'''
