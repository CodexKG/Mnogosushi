from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from apps.settings.models import Setting
from apps.users.models import User

# Create your views here.
def register(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if username and email and password and confirm_password:
                try:
                    user = User.objects.create(username = username, email = email)
                    user.set_password(password)
                    user.save()
                    user = User.objects.get(username = username)
                    user = authenticate(username = username, password = password)
                    login(request, user)
                    return redirect('index')
                except:
                    return redirect('register_error')
            else:
                return redirect('register_error')
        else:
            return redirect('register_error')
    context = {
        'setting' : setting,
    }
    return render(request, 'users/register.html', context)

def user_login(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
        except:
            return redirect('user_not_found')
    context = {
        'setting' : setting,
    }
    return render(request, 'users/login.html', context)

def profile(request, username):
    user = User.objects.get(username = username)
    setting = Setting.objects.latest('id')
    context = {
        'user' : user,
        'setting' : setting
    }
    return render(request, 'users/detail.html', context)