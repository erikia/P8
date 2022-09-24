from itertools import chain

from django.db.models import CharField, Value
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm

from review.models import Review
from ticket.forms import TicketForm
from ticket.models import Ticket
from user.models import User
from followers.models import UserFollows


def home(request):
    return render(request, 'index.html')

@login_required
def flux_view(request):
    reviews = get_all_reviews(request)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_all_tickets(request)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created,
                   reverse=True)
    answered_tickets = get_user_answered_tickets(request.user)
    return render(request,
                  'flux/flux.html',
                  context={
                      'posts': posts,
                      'answered_tickets': answered_tickets
                  })


def get_all_reviews(request):
    userfollows = get_user_follows(request.user)
    reviews_list = get_user_reviews(request.user)
    for userfollow in userfollows:
        user_reviews_list = get_user_reviews(userfollow.followed_user)
        reviews_list = reviews_list | user_reviews_list
        
    return reviews_list


def get_all_tickets(request):
    userfollows = get_user_follows(request.user)
    tickets_list = get_user_tickets(request.user)
    for userfollow in userfollows:
        user_tickets_list = get_user_tickets(userfollow.followed_user)
        tickets_list = tickets_list | user_tickets_list

    return tickets_list


def get_user_answered_tickets(userx):
    reviews_list = Review.objects.filter(user=userx)
    answers_list = []
    for review in reviews_list:
        answer = review.ticket
        answers_list.append(answer)
    return answers_list

@login_required
def abos_view(request):
    userfollows = get_user_follows(request.user)
    followers = get_user_followers(request.user)

    if request.method == "POST":
        requested_user = request.POST.get("search")
        if username_exists(requested_user):
            researched_user = search_user(requested_user)
            if researched_user != request.user:
                for userfollow in userfollows:
                    if userfollow.followed_user == researched_user:
                        return HttpResponse("You're already following this user")

                UserFollows.objects.create(user=request.user, followed_user=researched_user)
                return redirect('abos')

            else:
                return HttpResponse("Error")

        else:
            return HttpResponse(
                "Can't found the username"
            )

    return render(request, 'abos/abos.html', locals())

@login_required
def posts_view(request):
    reviews = get_user_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_user_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created,
                   reverse=True)

    return render(request, 'posts/posts.html', context={'posts': posts})


def get_user_reviews(userx):
    reviews_list = Review.objects.filter(user=userx)
    return reviews_list


def get_user_tickets(userx):
    tickets_list = Ticket.objects.filter(user=userx)
    return tickets_list


def create_user(request):
    username = request.POST.get("register_name")
    pass1 = request.POST.get("password1")
    pass2 = request.POST.get("password2")
    if pass1 == pass2 and not username_exists(username):
        User.objects.create_user(username, '', pass1)
        return HttpResponse(
            "Your account has been created.")
    elif pass1 != pass2:
        return HttpResponse(
            "The password doesn't match.")
    else:
        return HttpResponse("This username already exists")


def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def log_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('flux')
    else:
        return HttpResponse("Invalid account. Please try again;")


def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def modify_view(request, content_type, content_id):
    if request.method == "GET":
        if content_type == "REVIEW":
            try:
                requested_content = Review.objects.get(pk=content_id)
            except:
                return HttpResponse("This content is not available")
            if requested_content.user != request.user:
                return HttpResponse("You can't modify this content")
            form = ReviewForm(instance=requested_content)

        elif content_type == "TICKET":
            try:
                requested_content = Ticket.objects.get(pk=content_id)
            except:
                return HttpResponse("This content is not available")
            if requested_content.user != request.user:
                return HttpResponse("You can't modify this content")
            form = TicketForm(instance=requested_content)

        return render(request, 'ticket/modify.html', locals())
    elif request.method == "POST" and content_type == "REVIEW":
        instance_review = Review.objects.get(pk=content_id)
        form = ReviewForm(request.POST,
                          request.FILES,
                          instance=instance_review)
        if form.is_valid():
            form_review = form.save(commit=False)
            form_review.save()
        else:
            return render(request, 'ticket/modify.html', locals())
        return redirect('posts')
    elif request.method == "POST" and content_type == "TICKET":
        instance_ticket = Ticket.objects.get(pk=content_id)
        form = TicketForm(request.POST,
                          request.FILES,
                          instance=instance_ticket)
        form_ticket = form.save(commit=False)
        if form.is_valid():
            form_ticket = form.save(commit=False)
            form_ticket.save()
        else:
            return render(request, 'ticket/modify.html', locals())
        return redirect('posts')


def delete_view(request, content_type, content_id):
    if content_type == "REVIEW":
        requested_content = Review.objects.get(pk=content_id)
        requested_content.delete()

    elif content_type == "TICKET":
        requested_content = Ticket.objects.get(pk=content_id)
        requested_content.delete()

    return redirect('posts')


def get_user_follows(userx):
    follows_list = UserFollows.objects.filter(user=userx)
    return follows_list


def get_user_followers(userx):
    followers_list = UserFollows.objects.filter(followed_user=userx)
    return followers_list


def search_user(userx):
    user = User.objects.get(username=userx)
    return user


def unfollow_view(request, username):
    follow_delete = search_user(username)
    userfollow = UserFollows.objects.get(user=request.user,
                                         followed_user=follow_delete)
    userfollow.delete()

    return redirect('abos')