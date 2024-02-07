from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Profile
from . forms import UserForm

# Create your views here.
def loginUser(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, 'Username does not exist.')  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'page': page}
    return render(request, 'user/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out!')
    return redirect('login')


def registerUser(request):
    page= 'register'
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account successfully created.')
            login(request, user)
            return redirect('profiles')
        else:
            messages.success(request, 'An error has occurred during registrations.')
    context = {'page': page, 'form': form}
    return render(request, 'user/login_register.html', context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'user/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    top_skills = profile.skill_set.exclude(description__exact="")    # exclude data, doesn't have description
    other_skills = profile.skill_set.filter(description="")          # filter data, doesn't have description
    
    context = {'profile':profile, 'top_skills':top_skills, 'other_skills':other_skills}
    return render(request, 'user/user-profile.html', context)