from multiprocessing import context
import profile
from django.shortcuts import render, redirect
from .models import Profile
from django.http import HttpResponse
from .models import Project,Review,Tag
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .utils import searchProjects,paginateProjects
# projectsList = [

#     {
#         'id' : "1",
#         'title' : 'Ecommerce Website',
#         'description' : 'Fully function ecommerce website'
#     },
#     {
#         'id' : '2',
#         'title': 'Portfolio Website',
#         'description' : 'A personal website to write articles and display work'
#     },
#     {
#         'id' : '3',
#         'title' : 'Portfolio Website',
#         'description' : 'An open source project built by the community'
#     }
# ]

def projects(request):
    # projects=Project.objects.all().order_by('-vote_ratio','-vote_total')
    projects = searchProjects(request)
    page_projects, custom_range = paginateProjects(request, projects, 3)
    context = {
        'projects': page_projects,
        'custom_range': custom_range,

    }
    return render(request,'project/projects.html', context)

    

def project(request, pk):
    
    proj_obj = Project.objects.get(id=pk)

    tag= proj_obj.tag.all()
    reviews = proj_obj.review_set.all()

    form= ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.save()

            messages.success(request, 'Your review was submitted successfully ')
            return redirect('projects:project', pk=proj_obj.id)
        else:
            messages.error(request,'some error Occurred ')

    context = {'proj':proj_obj,'tags':tag, 'reviews': reviews,'form' : form}
    return render(request,'project/project.html',context)

@login_required(login_url='users:login')
def createProject(request):
    form=ProjectForm()

    if request.method == 'POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
           form.save()
           return redirect('projects:projects')

    context={'form':form,}
    return render(request,'project/project-form.html',context)

@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile
    projObj = profile.project_set.get(id=pk)

    form=ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form=ProjectForm(request.POST,instance=projectObj)        
        if form.is_valid():
           form.save()
           messages.success(request,'project updated successfully')
           return redirect('users:account')

    context={'form':form,}
    return render(request,'project/project-form.html',context)


@login_required(login_url='users:login')
def deleteProject(request, pk):
    profile = request.user.profile
    projObj = profile.project_set.get(id=pk)

   

    if request.method == 'POST':
       projObj.delete()   
       messages.success(request,'project deleted successfully')
       
       return redirect('users:account')

    context={'object': projObj}
    return render(request,'project/delete-template.html',context)




