from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from . models import Project
from . forms import projectForm, ReviewForm
from . utils import SearchProject, paginateProjects

# Create your views here.
def projects(request):
    projects, search_query = SearchProject(request)
    
    paginator, projects = paginateProjects(request, projects, 6)

    context = {'projects':projects, 'search_query':search_query, 'paginator':paginator}
    return render(request, 'projects/projects.html', context)

def Singleproject(request, pk):
    project = Project.objects.get(id=pk)
    
    print('Reviewers list: ', project.reviewers)
    
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            
            project.getVoteCount
            
            messages.success(request, 'Your review successfully submitted!')
            return redirect('project', pk=project.id)
            
    # Note: Need to make a signal to update vote count when delete review
    
    context = {'project':project, 'form':form}
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