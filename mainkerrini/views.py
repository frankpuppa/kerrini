from django.shortcuts import render, redirect, HttpResponse
from mainkerrini.models import User, UserLogin
from cassandra.cqlengine.query import LWTException
from django.core.exceptions import *
from mainkerrini.forms import RegisterForm, LoginForm

def index(request):
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = UserLogin.objects.get(email=form.cleaned_data['email_address'])
            request.session['user_loggedin'] = user.user_id
            return redirect('')
        else:
            raise ValidationError
            return redirect('/')
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

def register(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email_address'].lower()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # insert first/last name into user table
            try:
                # insert into userlogin if username is not taken
                UserLogin.if_not_exists().create(username=username, email=email, password=password)
                user = User.create(first_name=first_name, last_name=last_name)
                userlogin = UserLogin.objects.get(username=username)
                userlogin.user_id = user.user_id
                userlogin.save()
                return HttpResponse("done")
            except LWTException:
                return HttpResponse("LWT failed")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def search(request):
    return render(request, 'search.html')

def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
