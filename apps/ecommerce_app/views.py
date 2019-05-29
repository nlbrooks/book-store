from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def home(request):
    return render(request, "ecommerce_app/home.html")


def user_login(request):
    return render(request, "ecommerce_app/user_login.html")


def create_user(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/login")
        else:
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            email = request.POST['email']
            pw = request.POST['password']
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            this_user = User.objects.create(first_name=f_name, last_name=l_name, email=email, password=pw_hash)
            request.session['user'] = this_user.id
            return redirect("/")


def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/login")
        else:
            email = request.POST['email']
            this_user = User.objects.get(email=email)
            request.session['user'] = this_user.id
            return redirect("/")


def add_book(request):
    return render(request, "ecommerce_app/add_product.html")


def add_book_db(request):
    pass