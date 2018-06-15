from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from content.models import Content
from django.urls import reverse
import stripe
from django.conf import settings
#NEW MODELS TO BE MADE
#POINTS
#BANK ACCOUNT
#add uid to profile
#product
#blocked users



class Preview(models.Model):
    user = models.OneToOneField(User)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    #def get_absolute_url(self):
        #pass


class AccountRequest(models.Model):
    #user.requested.all() -> gives all the Requested invites and vise-versa
    userTo = models.ForeignKey(User, related_name='requested')
    userFrom = models.ForeignKey(User, related_name='requester')
    accept = models.BooleanField(default=False)
    sent = models.BooleanField(default=True)

    def __str__(self):
        return self.userTo.username

    def get_absolute_url(self):
        return reverse('account:detailAcceptance', kwargs={'name':self.userTo.username})

    def save(self, *args, **kwargs):
        if self.accept == True: #or self.userTo in self.userFrom.profile.following: #and user saving it is the userTo:
            self.userFrom.profile.following.add(self.userTo)
            self.delete()
            return None
        else:
            super(AccountRequest, self).save(*args, **kwargs)

class StripeCustomer(models.Model):
    user = models.OneToOneField(User)
    stripe_id = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)

class ConnectStripeAccount(models.Model):
    stripe_id = models.CharField(max_length=255)

class Profile(models.Model):
    # user.profile.following -- users i follow
    # user.followed_by -- users that follow me -- reverse relationship
    #if block end subscription and add a exclude blocked_by.all() when user searches
    following = models.ManyToManyField(User, blank=True, related_name='followed_by')
    blocked = models.ManyToManyField(User, blank=True, related_name='blocked_by')
    user = models.OneToOneField(User)
    age = models.DateTimeField(null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    link1 = models.URLField(null=True,  blank=True)
    link2 = models.URLField(null=True,  blank=True)
    location = models.CharField(max_length=150, null=True,  blank=True)
    pic = models.FileField(null=True,  blank=True)
    banner = models.FileField(null=True, blank=True)
    strikes = models.IntegerField(default=0,  blank=True)
    suspended = models.BooleanField(default=False)
    private = models.BooleanField(default=True)
    '''
    Genres = (('young','young'), ('mature', 'mature'), ('busty', 'busty'))
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)#this will be the primary key
    tier = models.PostiveIntegerField(default=1)
    genre = models.CharField(max_length=25, choices=Genres)
    percentage = models.PostiveIntegerField(default=25)

    '''

    def __str__(self):
        return self.user.username

    #to use in template -> object.get_absolute_url
    def get_absolute_url(self):
        return reverse('account:ProfileView', kwargs={'name':self.user.username})
'''
    def save(self):
        if self.tier == 1:
            self.percentage = 25
            self.save()
        elif self.tier == 2:
            self.percentage = 22
            self.save()
        elif self.tier == 3:
            self.percentage = 18
            self.save()
        else:
            self.percentage = 16
            self.save()
'''



def createProfile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(createProfile, sender=User)
