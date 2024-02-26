from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from . models import Profile
from . forms import UserForm, ProfileForm, SkillForm
from . utils import SearchProfiles, paginateProfiles

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
            return redirect('edit-account')
        else:
            messages.success(request, 'An error has occurred during registrations.')
    context = {'page': page, 'form': form}
    return render(request, 'user/login_register.html', context)


def profiles(request):
    profiles, search_query = SearchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles':profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'user/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    top_skills = profile.skill_set.exclude(description__exact="")    # exclude data, doesn't have description
    other_skills = profile.skill_set.filter(description="")          # filter data, doesn't have description
    
    context = {'profile':profile, 'top_skills':top_skills, 'other_skills':other_skills}
    return render(request, 'user/user-profile.html', context)


def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context = {'profile': profile, 'skills':skills, 'projects': projects}
    return render(request, 'user/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'user/profile_form.html', context)

@login_required(login_url='login')
def addSkill(request):
    page = 'add'
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
            
    context={'form':form, 'page': page}
    return render(request, 'user/skill_form.html', context)

@login_required(login_url='login')
def editSkill(request, pk):
    page = 'edit'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
        
    context = {'form':form, 'page': page}
    return render(request, 'user/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {'obj': skill}
    return render(request, 'projects/delete_objects.html', context)