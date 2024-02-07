from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . models import Project
from . forms import projectForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)

def Singleproject(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project':project}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    form = projectForm()
    
    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # project = form.save(commit=False)         # Issue duraing create a project, User is Null save in database insteed of user id
            # project.owner = request.user.profile
            # project.save()
            return redirect('projects')
    
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = projectForm(instance=project)
    
    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'obj':project}
    return render(request, 'projects/delete_objects.html', context)