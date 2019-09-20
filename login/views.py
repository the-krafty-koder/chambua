from django.shortcuts import render
from .form import login_form, signup_form
from django.contrib.auth import authenticate, login, logout
from .backends import AuthBackend
from django.shortcuts import redirect,render
from django.http import HttpResponse
from .models import *
import random


# Create your views here.

def loginto(request):
    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user_auth = authenticate(username = cd['name'], password = cd['password'], institution_id = cd['institution_id'])

            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    return redirect('/home')
                else:
                    return HttpResponse('User disabled')
            else:
                return HttpResponse("User is not valid")
        else:
            form = login_form
            return HttpResponse("Enter form correctly")
    else:
        form = login_form()

    return render(request, 'login.html', {'form':form})

def complete(request):
    return redirect('/logout')


def signup(request):
    if request.method == "POST":

        form = signup_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            id = random.randint(1000,100000)
            Users.objects.create_user(cd["institution_name"],cd["email"],id,cd["password"])

            user = Users.objects.get(name=cd["institution_name"])
            return render(request, "sucess.html", {'user': user})

    else:
        form = signup_form()

    return render(request,"signup.html",{"form":form})

def get_det(request):
    user = Users.objects.get(name="Golden Academy")
    return render(request, "sucess.html", {'user': user})


def logout_view(request):
    logout(request)
    return redirect('/home')
