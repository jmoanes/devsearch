from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag #Include tag for SearchTag
from .forms import projectForm
from django.contrib.auth.decorators import login_required # only authenticated user can access the Add Project form when they login import

from django.db.models import Q



def projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    

    project = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    context = {'projects': project, 'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    proObj = Project.objects.get(id=pk)
    return render(request, 'projects/single_project.html', {'project': proObj})
# Noted:  proceed to Flash messages after @login_required(login_url='login')



@login_required(login_url='login') # only authenticated user can access the Add Project form when they login
def createProject(request):
    profile = request.user.profile #dont put this code until you didnt add project yet on the create-project form

    form = projectForm()

    if request.method == 'POST':
        form = projectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile #dont put this code until you didnt add project yet on the create-project form
            project.save() #dont put this code until you didnt add project yet on the create-project form
            return redirect('projects')  # PROCCEED TO DELETE VIEWS
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)



@login_required(login_url='login') # only authenticated user can access the Add Project form when they login
def updateProject(request, pk):
    profile = request.user.profile #Code only login user can edit the project 
    project = profile.project_set.get(id=pk) #Code only login user can edit the project 
    # project = Project.objects.get(id=pk)     # PROCCEED TO DELETE VIEWS 
    form = projectForm(instance=project)

    if request.method == 'POST':
        form = projectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)



@login_required(login_url='login') # only authenticated user can access the Add Project form when they login
def deleteProject(request, pk):
    profile = request.user.profile #Code only login user can delete the project 
    project = profile.project_set.get(id=pk) #Code only login user can edit the project 
    # project = Project.objects.get(id=pk)   # PROCEED TO ADD, DELETE, EDIT sKILLS

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'projects/delete-project.html', context)







#**********NOTED: AFTER VIEWS PROCEED TO URLS****************# 