from django.shortcuts import render, redirect, Http404
from content.models import Content, Comment, Like
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
from .forms import Reporter
from django.db.models import Q

def index(request):
    followers = request.user.profile.following.all()
    #followers.append(user)
    queryset_list = Content.objects.filter(user__in=followers).order_by('-date')
    return render(request, 'banking/n.html', {'queryset_list':queryset_list})


def SearchUser(request):
    query = request.GET.get('q')
    if query:
        queryset_list = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(location__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
        ).distinct()
        return render(request, 'home/SearchUser.html', {'queryset_list':queryset_list})
    else:
        return None

def discoverView(request):
    page = 'Spotlight'
    users = User.objects.filter('?')[:24]
    return render(request, 'home/discover.html', {'users':users, 'page':page})

def discoverGenre(request, genre):
    try:
        users = Profile.objects.filter(genre_exact=genre)[:24]
    except Profile.DoesNotExist:
        raise http404('cant find any users under this genre')
    page = genre
    return render(request, 'home/genreUsers.html', {'users':users, 'page':page})

class emailReport(FormView):
    template_name = 'home/contact.html'
    form_class = Reporter
    success_url = '/home/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(emailReport, self).form_valid(form)


'''
class BugReport(emailReport):
    we dont need their email
    user makes the message, subject is always bug
    pass

class ViolationReport(emailReport):
    we dont need their email
    should just be choice:
    ex.
    illegal content
    slander
    bullying
    offensive
    missed advertised
    aggresive or endangering of human/animal
    copyright
    and then grabs a screenshot of the violation
    pass

class ContactReport(emailReport):
    user makes subject and message
    we need their email
    this is for potential users or celebs
    pass

class SupportReport(emailReport):
    user makes subject and message, and the users account
    we need their email
    this is for paid users, about their account or using the service
    pass
'''
