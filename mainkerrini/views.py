from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from mainkerrini.custom_functions import *
from mainkerrini.forms import RegisterForm
from .forms import UploadFileForm

import uuid
import re
import magic
import datetime


import os

from django.shortcuts import render, redirect, HttpResponse
from kerrini.settings import PIC
from mainkerrini.models import *
from cassandra.cqlengine.query import LWTException
from mainkerrini.forms import *
from django.core.files.base import ContentFile

def index(request):
    form = LoginForm()
    return render(request, 'index.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = UserLogin.objects.get(email=form.cleaned_data['email_address'])
            request.session['user_id'] = user_login.user_id
            request.session['username'] = user_login.username
            return redirect('/profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email_address'].lower()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                # insert into userlogin if username is not taken
                UserLogin.if_not_exists().create(username=username, email=email, password=password)
                user = User.create(first_name=first_name, last_name=last_name)
                user_login = UserLogin.objects.get(username=username)
                user_login.user_id = user.user_id
                user_login.save()
                request.session['user_id'] = user_login.user_id
                request.session['username'] = user_login.username
                return redirect('/profile')
            except LWTException:
                return HttpResponse("LWT failed")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def upload(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            storage = FileSystemStorage(
                    location = '/tmp/django',
                    base_url = '/tmp/django'
                  )
            content = request.FILES['file']
            name = storage.save(None, content)
            url = storage.url(name)
            #print(url)
            filetype = magic.from_file(url,mime=True).decode()
            myreg=re.compile(r'(mp4)|(ogg)|(webm)',re.I)
            ext=myreg.search(filetype)
            if ext:
                newfilename=move_file(url,ext.group(0).lower())
            # if hasattr(file, '/tmp/'):
                 #filetype = magic.from_file(file.temporary_file_path(),mime=True).decode()
            # else:
            #     filetype = magic.from_buffer(file.read(),mime=True).decode()
            # myreg=re.compile(r'(mp4)|(ogg)|(webm)',re.I)
            # ext=myreg.search(filetype)
           # print(filetype)
                dir=ext.group(0).lower()
            # newfilename=handle_uploaded_file(file, dir)
            # #print(newfilename)
                data=dir + "/" + str(newfilename)
                try:
                     Video.create(video_id=newfilename, correctness=0, title=form.cleaned_data['title'], description=form.cleaned_data['description'], data=data, date_created=datetime.datetime.now(),video_codec=dir)
                except Video.DoesNotExist:
                     return HttpResponse("LWT failed")
        return render(request,'upload.html', {'form':form})
    else:
        form = UploadFileForm()
    return render (request,'upload.html', {'form': form})


def play(request):
    return render(request, 'play.html')


def profile(request):
    try:
        user = User.objects.get(user_id=request.session['user_id'])
        user_login = UserLogin.objects.get(username=request.session['username'])
        try:
            picture = Picture.objects.get(user_id=user.user_id)
        except Picture.DoesNotExist:
            picture =  Picture(data='images/avatar.jpg', user_id=user.user_id)
    except(KeyError, User.DoesNotExist):
        redirect('/login')
    return render(request, 'profile.html', {'user_login': user_login, 'user': user, 'picture': picture})

def edit(request):
    user = User.objects.get(user_id=request.session['user_id'])
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            bio = form.cleaned_data['bio']
            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio
            user.save()
            return redirect('/edit')
    else:
        form = AccountForm(initial={'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'bio': user.bio})
        try:
            picture = Picture.objects.get(user_id=user.user_id)
        except Picture.DoesNotExist:
            picture =  Picture(data='images/avatar.jpg', user_id=user.user_id)
    return render(request, 'edit.html', {'form': form, 'picture': picture})

def logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except KeyError:
        redirect("/login/")
    return redirect("/")

def picture(request):
    print("in picture")
    if request.method == 'POST':
        print("in post")
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            folder = 'profile_pics'
            uploaded_filename = request.session['username'] + '.' + request.FILES['image'].name
            # create the folder if it doesn't exist.
            try:
                os.makedirs(os.path.join(PIC, folder))
            except:
                pass
            # save the uploaded file inside that folder.
            db_path = folder + '/' + uploaded_filename
            full_filename = os.path.join(PIC, folder, uploaded_filename)
            fout = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES['image'].read())
            try:
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                try:
                    picture = Picture.objects.get(user_id=request.session['user_id'])
                    picture.user_id = request.session['user_id']
                    picture.data = db_path
                    picture.save()
                    print("in try")
                except Picture.DoesNotExist:
                    Picture.create(user_id=request.session['user_id'], data=db_path)
                    print("does not exist")
            except:
                return redirect('/picture')
            return redirect('/profile')
    else:
        form = ImageForm()
    return render(request, 'uploadimage.html', {'form': form})

def search(request):
    return render(request, 'search.html')

def search_result(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

