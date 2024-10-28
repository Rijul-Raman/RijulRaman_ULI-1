from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'tasks/login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed  
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect('task_list')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        Task.objects.create(title=title, description=description, user=request.user)
        messages.success(request, 'Task created successfully!')
        return redirect('task_list')
    return render(request, 'tasks/create_task.html')

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')
    return render(request, 'tasks/update_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')
