from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Projectebi, Tag
from .forms import ProjectForm, ReviewForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import search_project, paginate_projects




def index(request):
    projects, search_query = search_project(request)
    custom_rage, projects = paginate_projects(request, projects, 6)
    context = {"all_projects": projects, 'search_query': search_query, 'custom_range': custom_rage}
    return render(request, 'my_app/main.html', context)
    # ას custom_rage, projects = paginate_projects(request, projects, 6)-ში 6-იანი არის კარტების რაოდენობა
    # რაც ერთ გვერდზე უნდა გამოჩნდეს.
    # custom_rage და projects მიიღებენ მნიშვნელობებს paginate_projects ფუნქციიდან რომელიც utils.py-ში არიან
    # თითოეული აპისთვის




def projects(request, pk):
    project_object = Projectebi.objects.get(id=pk)
    # ეს არის ერტი კონკრეტული პროექტი იმიტომ რომ id=pk-ს და აიდით განვსაზღვრეთ კონკრეტულად რომელია
    form = ReviewForm()
    #tags = project_object.tags.all()
    #return render(request, 'my_app/projects.html', {'project': project_object, "tags": tags})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.projecti = project_object
        review.owner = request.user.profile
        review.save()
        project_object.get_vote_count
        # get_vote_count არის ფუქცია project ის მოდელებში რომელიც თვლის რივიუებს და პროცენტებს.
        # აქ რატოა ყვითლად არ ვიცი
        messages.success(request, 'your comment was successfully submitted!')
        return redirect('projects', pk=project_object.id)
        # ეს return redirect('projects', pk=project_object.id) ცამოუტვირთვას იუზერს პროექტის გვერდს თავიდან
        # კომენტარის დაწერის შემდეგ თავისი დაწერილი კომენტარი რო გაქრეს ტექსტბოქსიდან

    context = {'project': project_object, 'form': form}
    return render(request, 'my_app/projects.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile   # ეს, ზედა და ქვედა ხაზები მიაკუთვნებენ პროექტს ვისი პროფილიდანაც შექმნება იმას
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, 'my_app/project_form.html', context)



def update_project(request, pk):
    profile = request.user.profile               # ეს ორი ხაზი გვჭორდება იმისვთის რო მარტო პროდუქტის მფლობელს შეეძლოს
    project = profile.projectebi_set.get(id=pk)  # საკუთარი პროდუქტის დაედითება  და სხვას არა რომელსაც პროდუქტის აიდი აქვს
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('home')
    context = {'form': form, 'project': project}
    return render(request, 'my_app/project_form.html', context)



def delete_project(request, pk):
    profile = request.user.profile
    dlt_project = profile.projectebi_set.get(id=pk)
    if request.method == 'POST':
        dlt_project.delete()
        messages.success(request, 'Project was deleted successfully')
        return redirect('account')
    context = {'object': dlt_project}
    return render(request, 'delete_template.html', context)
