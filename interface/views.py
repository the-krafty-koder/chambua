from django.shortcuts import render,redirect
from login.models import *

def home(request):
    x = redirect
    return render(request,"home.html",{'login':redirect('/login')})

