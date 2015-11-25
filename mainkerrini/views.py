from django.shortcuts import render, redirect
from mainkerrini.custom_functions import *

from mainkerrini.forms import RegisterForm
from .forms import UploadFileForm


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, '')


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            return redirect('/kerri/index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            handle_uploaded_file(file)
            return render(request,'upload.html', {'file':file, 'form':form})
    else:
        form = UploadFileForm()
    return render (request,'upload.html', {'form': form})


def testvideo(request):
    return render(request, 'testvideo.html')