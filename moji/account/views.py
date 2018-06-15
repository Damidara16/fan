from django.shortcuts import render, redirect
from account.models import Profile, AccountRequest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from .forms import RegistrationForm, EditProfileForm, UpdateUserForm, RequestForm
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View

#ACCOUNT SUITE

def blockUser(request, name=None):
    user = User.objects.get(username=name)
    request.user.profile.following.remove(user)
    request.user.followed_by.remove(user)
    request.user.profile.blocked.add(user)
    return redirect(reverse('home:home'))
    #take the user and current user,
    #1. blocked the user by adding to blocked list
    #2. remove user from following

def unblockUser(request, name=None):
    user = User.objects.get(username=name)
    request.user.profile.blocked.remove(user)
    return redirect(reverse('home:home'))


def ViewProfile(request, name=None):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if name == request.user.username:
        return render(request, "account/OwnerProfile.html", {"user":user})
    elif user.profile.private and user not in request.user.profile.following.all():
        return render(request, "account/PrivateProfile.html", {"user":user})
    else:
        return render(request, "account/profile.html", {"user":user})

def updateProfile(request):
    if request.method  == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        form1 = UpdateUserForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form1.is_valid():
            profile = form.save(commit=False)
            profile1 = form1.save(commit=False)
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.email = form.cleaned_data['email']
            profile1.age = form1.cleaned_data['age']
            profile1.bio = form1.cleaned_data['bio']
            profile1.pic = form1.cleaned_data['pic']
            profile1.banner = form1.cleaned_data['banner']
            profile1.link1 = form1.cleaned_data['link1']
            profile1.link2 = form1.cleaned_data['link2']
            profile1.private = form1.cleaned_data['private']
            profile1.location = form1.cleaned_data['location']
            profile.save()
            profile1.save()
            return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))
    else:
        form = EditProfileForm(instance=request.user)
        form1 = UpdateUserForm(instance=request.user.profile)
        return render(request, 'account/update.html', {'form':form, 'form1':form1})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #return render(request, 'account/profile.html')
            return redirect(reverse('account:login'))
        else:
            return redirect(reverse('account:login'))
    else:
        form = RegistrationForm()
        return render(request, 'account/req.html', {'form':form})

def deleteProfile(request):
    #add a re-enter passcode to delete account
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('/home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('content:CreatePost'))
        else:
            return redirect(reverse('account:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'account/password.html', args)


#PREVIEW SUITE
def PreviewAdd(request, id):
    content = Content.object.get(id=id)
    Preview.objects.create(user=request.user, content=content)
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def PreviewRemove(request, id):
    Preview = Preview.object.get(id=id)
    Preview.delete()
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))


#FOLLOW SUITE

def listRequests(request):
    user = request.user
    return render(request, 'account/reqList.html', {'user':user})

def detailRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userTo=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return render(request, 'account/reqDetail.html', {'req':req})

def deleteRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userTo=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
        req.delete()
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def editRequests(request, name):
    try:
        user = User.objects.get(username=name)
        req = request.user.requested.get(userTo=user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
        req.accept = True
        req.save()
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def makeRequests(request, name):
    #need to add where one model can be made, probably use the sent field
    try:
        user = User.objects.get(username=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that request")
    accept = AccountRequest()
    accept.userTo = user
    accept.userFrom = request.user
    accept.save()
    return redirect(reverse('account:ProfileView', kwargs={'name':request.user.username}))

def unfollowUser(request, name):
    try:
        user = User.objects.get(username=name)
        request.user.profile.following.remove(user)
        #req = AccountRequest.objects.filter(userFrom=request.user).get(userTo=name)
    except AccountRequest.DoesNotExist:
        raise Http404("Cant find that user")
    return redirect(reverse('home:home'))
