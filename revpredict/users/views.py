import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('django')
def sign_in(request):
    try:
        logger.info("sign_in view was called")
        if request.method == 'GET':
            if request.user.is_authenticated:
                return redirect('home')

            form = LoginForm()
            return render(request, 'users/login.html', {'form': form, 'title':'Sign in'})

        elif request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Successfully authenticated as {username.title()}')
                    logger.info(f'Successfully authenticated as {username.title()}')
                    return redirect('home')

            # form is not valid or user is not authenticated
            messages.error(request, f'Invalid username or password')
            logger.error(f'Invalid username or password')
            return render(request, 'users/login.html', {'form': form, 'title':'Sign in'})
    except Exception as e:
        logger.exception("Exception occuried in sign_in view")

def sign_out(request):
    try:
        logout(request)
        messages.success(request,f'You have been logged out.')
        logger.info(f"{request.user} have been logged out.")
        return redirect('login')
    except Exception as ex:
        logger.exception("Exception occured in sign_out view")


def index(request):
    logger.info("index view was called")
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'users/index.html', context=context)


@login_required
def about(request):
    try:
        logger.info("about view was called")
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                logger.info(f" {request.user }'s Profile was successfully updated")
                return redirect('about')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
    except Exception as e:
        logger.exception("Exception occured in about view")

def sign_up(request):
    try:
        logger.info("sign_up view was called")
        if request.method == 'GET':
            form = RegisterForm()
            return render(request, 'users/register.html', { 'form': form, 'title':'Sign up'})

        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have singed up successfully.')
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'users/register.html', {'form': form, 'title':'Sign up'})
    except Exception as e:
        logger.exception("Exception occured in sign_up view")