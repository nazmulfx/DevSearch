from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from . models import Project
from . forms import projectForm
from . utils import SearchProject

# Create your views here.
def projects(request):
    projects, search_query = SearchProject(request)
    
    page = request.GET.get('page')                      # getting data from user like ?page=1
    objectPerPage = 1
    paginator = Paginator(projects, objectPerPage)
    
    try:                                                # if everything is good like url/?page=2
        projects = paginator.page(page)                 
    except PageNotAnInteger:                            # if page number not given like url/
        page = 3
        projects = paginator.page(page)
    except EmptyPage:                                   # if user accidently goes wrong page number like url/?page=100000
        page = paginator.num_pages
        projects = paginator.page(page)
        
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
        
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
        
    custom_range = range(leftIndex, rightIndex)
    
    context = {'projects':projects, 'search_query':search_query, 'paginator':paginator, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)

def Singleproject(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project':project}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = projectForm()
    
    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project Created Successfully!')
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = projectForm(instance=project)
    
    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Updated Successfully!')
            return redirect('account')
    
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project Deleted Successfully!')
        return redirect('account')
    
    context = {'obj':project}
    return render(request, 'projects/delete_objects.html', context)