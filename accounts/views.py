from urllib import request
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreationForm, SignUpForm
from django.contrib.auth import authenticate


def login_user(request):    
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = authenticate(request, username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.warning(request, 'Invalid Credentials')

        context = {}
        return render(request, 'accounts/login.html', context)

def logout_user(request):
    logout(request)
    # messages.info(request, "you are logged out")
    return redirect('/')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = SignUpForm()

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user_name)
                return redirect('/accounts/login')
            else:
                messages.warning(request, 'Invalid Registration')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

    