from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from . models import Profile
from . forms import UserForm, ProfileForm, SkillForm, MessageForm
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')    # if url have 'next' GET request, after login redirect to 'next=URL' otherwise redirect user to their account page
            # return redirect(
            #     if 'next' in request.GET:
            #         request.GET['next']
            #     else:
            #         'account'   
            # )
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
    
    paginator, profiles = paginateProfiles(request, profiles, 6)
    
    context = {'profiles':profiles, 'search_query':search_query, 'paginator':paginator}
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


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messages_request = profile.message_recipient.all()                # querying child model by related name from Message model 'ForeignKey'
    unread_messages = messages_request.filter(is_read=False).count()  # counting unread messages
    context = {'messages_request':messages_request, 'unread_messages':unread_messages}
    return render(request, 'user/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile                  # step-1: querying loged in user profile (just limiting that only logged in user can query his own messages)
    message = profile.message_recipient.get(id=pk)  # step-2: querying profile>message_recipient by the Message Model id
    
    if message.is_read == False:                    # step-: only it will call when it unread
        message.is_read = True                     # step-1: if user read the message is_read = True then save
        message.save()
        
    context = {'message':message}
    return render(request, 'user/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)          # getting recipient id by url from recipient profile
    form = MessageForm()
    
    try:                                            # try catch: to check if the user is loged in or not
        sender = request.user.profile               # getting sender id from request object
    except:
        sender = None                               # if anonymous then sender is none (extra 3 field add ['name', 'email', ''])
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent.')
            return redirect('user-profile', pk=recipient.id)
    
    context = {'recipient': recipient, 'form':form}
    return render(request, 'user/message_form.html', context)