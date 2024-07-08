from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from .models import Mailing, Client, Message, BlogPost
from .forms import MailingForm, ClientForm, MessageForm
from random import sample


@login_required
def mailing_list(request):
    mailings = Mailing.objects.filter(owner=request.user)
    return render(request, 'mailing/mailing_list.html', {'mailings': mailings})


@login_required
def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner != request.user:
        return HttpResponseForbidden()
    return render(request, 'mailing/mailing_detail.html', {'mailing': mailing})


@login_required
def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form.save_m2m()
            return redirect('mailing_list')
    else:
        form = MailingForm()
    return render(request, 'mailing/mailing_form.html', {'form': form})


@login_required
def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing_list')
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'mailing/mailing_form.html', {'form': form})


@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing_list')
    return render(request, 'mailing/mailing_confirm_delete.html', {'mailing': mailing})


@cache_page(60 * 15)
def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_clients = Client.objects.values('email').distinct().count()
    blog_posts = list(BlogPost.objects.all())
    random_posts = sample(blog_posts, 3) if len(blog_posts) >= 3 else blog_posts
    return render(request, 'mailing/index.html', {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_posts': random_posts,
    })


def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'mailing/blog_list.html', {'posts': posts})


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'mailing/blog_detail.html', {'post': post})
