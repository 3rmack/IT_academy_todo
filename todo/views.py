# coding: UTF-8
from django.shortcuts import render
from models import Tasks
from forms import TaskForm


def index(request):
    tasks = Tasks.objects.filter()
    context = {'tasks': tasks}
    return render(request, 'index.html', context)


def add_task(request):
    if request.method == 'POST':
        raw_data = TaskForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data
            Tasks.objects.create(**data)
    else:
        context = {'task_add_form': TaskForm()}
        return render(request, 'task_add_form.html', context)

