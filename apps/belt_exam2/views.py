from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from .models import User, Quote, Favorited

# Create your views here.
def index(request):
    return render(request, 'belt_exam2/index.html')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid Login Credentials")
        else:
            request.session['logged_user'] = user.id
            # messages.success(request, "Welcome {}!".format(user.first_name))
            return redirect('/quotes')

    return redirect ('/main')

def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate_user_info(request.POST)
        #if there are errors throw them into the flash messages list
        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
                print form_errors
        else:
            user = User.objects.register(request.POST)
            messages.success(request, "You have successfully registered! Please sign-in to continue.")

        return redirect('/main')

def logout(request):
    if 'logged_user' not in request.session:
        request.session.pop('logged_user')
    return redirect('/main')


def quotes(request):
    current_user = User.objects.get(id=request.session['logged_user'])
    current_user_favorites = Quote.objects.filter(favorite_quote__favoritor=current_user)
    all_quotes = Quote.objects.all().exclude(id__in=current_user_favorites)

    # current_user = User.objects.get(id=request.session['logged_user'])
    # all_quotes = Quote.objects.all()
    # current_user_favorites = Quote.objects.filter(favorite_quote__favoritor=current_user)
    # test = all_quotes | current_user_favorites
    # other_users_quotes = Quote.objects.exclude(id__in=test)
    # Trip.objects.exclude(id__in=my_trips)

    context = {
        "current_user": current_user,
        "all_quotes": all_quotes,
        "current_user_favorites": current_user_favorites,
    }

    return render(request, 'belt_exam2/quotes.html', context)

def add_quote(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Gotta login bro.")
        return redirect('/adminlogin')

    if request.method == "POST":
        form_errors = Quote.objects.validate_quote_info(request.POST)
        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
                print form_errors
                return redirect('/quotes')
        else:
            current_user = request.session['logged_user']
            Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], user_id=current_user)
            messages.success(request, "Posted to the quote wall!")
    return redirect('/quotes')

def favorite(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    quote = Quote.objects.get(id=id)
    favorite_quote = Favorited.objects.create(favoritor=user, quote=quote)

    return redirect('/quotes')

def remove_favorite(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    quote = Quote.objects.get(id=id)
    favorite_quote = Favorited.objects.filter(favoritor=user, quote=quote).delete()
    return redirect('/quotes')

def user_profile(request, id):
    if 'logged_user' not in request.session:
        messages.error(request, "Gotta login bro.")
        return redirect('/adminlogin')

    user_name = User.objects.get(id=id)
    all_users_posts = Quote.objects.filter(user=id)
    user_post_count = all_users_posts.count()

    context = {
        "all_users_posts": all_users_posts,
        "user_post_count": user_post_count,
        "user_name": user_name
    }

    return render(request, 'belt_exam2/user.html', context)
