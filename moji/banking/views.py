from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import json
from django.conf import settings
from content.models import Content

def number1(request):
    #in templates after successful creation, change button to edit payout info
    return render(request, 'banking/bank.html')

def number2(request):
    Acode = request.GET.get('code')
    if Acode:
        data = [
        ('client_secret', 'sk_test_KfXaKQvXftN0sR3GfoDLQhfs'),
        ('code', Acode),
        ('grant_type', 'authorization_code'),
        ]

    response = requests.post('https://connect.stripe.com/oauth/token', data=data)
    if response.status_code == 200:
        a = json.loads(response.text)
        #ConnectStripeAccount.objects.create(stripe_id=(a['stripe_user_id']), ...)
    else:
        #error response
        None
    #return redirect(reverse('account:ProfileView', kwargs={'user':request.user.get_absolute_url))

def number3(request):
    source = request.POST.get('stripeToken')
    return render(request, 'banking/token.html', {'source':source})


def new(request):
    item = Content.objects.filter()[2]
    user = request.user
    return render(request, 'banking/n.html', {'item':item, 'user':user})
