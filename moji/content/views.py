from django.shortcuts import render, redirect, Http404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from content.models import Content, Comment
from product.models import Points, PointsWallet
from django.urls import reverse
from .forms import CommentForm, LikeForm

def detailContent(request, id):
    try:
        content = Content.objects.get(id=id)
    except Content.DoesNotExist:
        raise Http404('cant find this content')
    if content.user not in request.user.profile.following.all():
        return redirect('account:ProfileView')
    return render(request, 'home/detail.html', {'content':content})


#need to get item and then delete
def deleteContent(request, id):
    content = Content.objects.get(id=id)
    content.delete()
    return redirect(reverse('content:CreatePost'))

def deleteComment(request, id):
    content = Comment.objects.get(id=id)
    content.delete()
    a = request.user.pointswallet_set.get(name=post.user.username)
    a.amount -= post.user.points.comment
    a.save()
    return redirect(reverse('home:home'))

def deleteLike(request, id):
    content = Like.objects.get(id=id)
    content.delete()
    #this is how points are deleted when unliking
    a = request.user.pointswallet_set.get(name=post.user.username)
    a.amount -= post.user.points.like
    a.save()
    return redirect(reverse('home:home'))

#need to handle unauthorized user, use middleware
class postCreate(CreateView):
    model = Content
    fields = ['file', 'caption']
    template_name = 'content/make.html'
    success_url = '/content/create/post'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.typeContent = 'Post'
        return super(postCreate, self).form_valid(form)

class videoCreate(CreateView):
    model = Content
    fields = ['file', 'caption', 'thumbnail']
    template_name = 'content/make.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.typeContent = 'Video'
        return super(videoCreate, self).form_valid(form)


class tweetCreate(CreateView):
    model = Content
    fields = ['caption',]
    template_name = 'content/make.html'
    #success_url = reverse('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.typeContent = 'Tweet'
        return super(tweetCreate, self).form_valid(form)

def commentCreate(request, pk):
    try:
        post = Content.objects.get(pk=pk)
    except Content.DoesNotExist:
        raise Http404('this content does not exist, sorry')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ParentContent = post
            comment.user = request.user
            comment.comment = form.cleaned_data['comment']
            comment.save()
            a = request.user.pointswallet_set.get(name=post.user.username)
            a.amount += post.user.points.comment
            a.save()
            return redirect(reverse('content:detail', kwargs={'id':post.id}))
    else:
        form = CommentForm()
    return render(request, 'content/make.html', {'form': form})

def likeCreate(request, pk):
    try:
        post = Content.objects.get(pk=pk)
    except Content.DoesNotExist:
        raise Http404('this content does not exist, sorry')
    if request.method == "POST":
        form = LikeForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ParentContent = post
            comment.user = request.user
            comment.like = form.cleaned_data['like']
            comment.save()
            #this is how points are added
            a = request.user.pointswallet_set.get(name=post.user.username)
            a.amount += post.user.points.like
            a.save()
            return redirect(reverse('content:detail', kwargs={'id':post.id}))
    else:
        form = LikeForm()
    return render(request, 'content/make.html', {'form': form})
