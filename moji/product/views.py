'''from django.shortcuts import render
from .models import Tip, Reward, PointsWallet, Points, Plan
from .form import SetPoint
from django.views.generic.edit import CreateView
#CRUD PLAN
#HANDLES MAKING A NEW PLAN, UPDATING AN EXISTING, AND DELETING A CURRENT PLAN
class CreatePlan(CreateView):
    model = Plan
    fields = ['price', 'name', 'description']
    template_name = 'content/make.html'
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(postCreate, self).form_valid(form)

class CreatePoints(CreateView):
    model = Points
    fields = ['like', 'comment']
    template_name = 'content/make.html'
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(postCreate, self).form_valid(form)

class PointsUpdate(UpdateView):
    model = Points
    fields = ['like', 'comment']
    template_name_suffix = 'content/make.html'

#CRUD PRODUCT

#CRUD SUBSCRIPTION
#HANDLES A USER PAYING FOR A SUBSCRIPTION, RETRIEVE SUBSCRIPTION, AND CANCELLING A SUBSCRIPTION
def addSub(request, user):
    a = stripe.Subscription.create(
    customer = request.user.stripe_customer.stripe_id,
    plan = user.plan_set.filter()[0],
    application_fee_percent=user.profile.percentage,
    stripe_account = user.stripe_account.stripe_id
    )
    if a['status'] == 'success':
        request.user.following.add(user)
    else:
        return a['status'], a['outcome']['reason']
#CRUD TIP


#CRUD REWARDS


def ClaimReward(request):
    pass

def GainPoints(request, name):
    user = User.objects.get(username=name)
    Points = PointsWallet.objects.filter(user=user).get(owner=request.user)
    if action is like:
        Points.amount += user.points.likes
        Points.save()
    elif action is comment:
        Points.amount += user.points.comment
        Points.save()
    else:
        return None

def SendTip(request, user):
    pass

def SetPoints(request):
    if request.method  == "POST":
        form = SetPoint(request.POST, instance=request.user.points)
        if form.is_valid():
            point = form.save(commit=False)
            point.likes = form.cleaned_data['likes']
            point.comment = form.cleaned_data['comment']
            point.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    else:
        form = SetPoint(instance=request.user.points)
        return render(request, 'account/update.html', {'form':form})

'''
