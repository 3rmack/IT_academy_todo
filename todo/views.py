# coding: UTF-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import Tasks
from forms import TaskForm


def index(request):
    tasks = Tasks.objects.filter().order_by('order')
    context = {'tasks': tasks}
    return render(request, 'index.html', context)


def add_task(request):
    if request.method == 'POST':
        raw_data = TaskForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data

            if Tasks.objects.filter().order_by('order').last():
                last_task = Tasks.objects.filter().order_by('order').last()
                Tasks.objects.create(order=last_task.order+1, **data)
            else:
                Tasks.objects.create(order=1, **data)

            return redirect(index)
        else:
            context = {'message': 'You input a bad task name'}
            return render(request, 'error.html', context)
    else:
        context = {'task_add_form': TaskForm()}
        return render(request, 'task_add_form.html', context)


def updown(request):
    task_to_modify = request.GET
    if task_to_modify['type'] == 'up':
        task_to_move_up = Tasks.objects.get(order=task_to_modify['order'])
        if task_to_move_up.order == 1:
            return redirect(index)
        else:
            task_to_move_down = Tasks.objects.get(order=int(task_to_modify['order'])-1)
            task_to_move_up.order = task_to_move_down.order
            task_to_move_down.order = task_to_modify['order']
            task_to_move_up.save()
            task_to_move_down.save()
            return redirect(index)
    elif task_to_modify['type'] == 'down':
        last_task = Tasks.objects.filter().order_by('order').last()
        task_to_move_down = Tasks.objects.get(order=task_to_modify['order'])
        if task_to_move_down.order == last_task.order:
            return redirect(index)
        else:
            task_to_move_up = Tasks.objects.get(order=int(task_to_modify['order'])+1)
            task_to_move_up.order = task_to_move_down.order
            task_to_move_down.order = int(task_to_modify['order']) + 1
            task_to_move_up.save()
            task_to_move_down.save()
            return redirect(index)


def edit(request):
    if request.method == 'POST':
        task_to_modify = request.POST
        task = Tasks.objects.get(id=task_to_modify['id'])
        if task_to_modify['task']:
            task.task = task_to_modify['task']
        else:
            context = {'message': 'You input a bad task name'}
            return render(request, 'error.html', context)
        if 'status' in task_to_modify:
            task.status = True
        else:
            task.status = False
        task.save()
        return redirect(index)
    else:
        task_to_modify_id = request.GET.get('id')
        task_to_modify = Tasks.objects.get(id=int(task_to_modify_id))
        context = {'task': task_to_modify}
        return render(request, 'task_edit_form.html', context)


def delete(request):
    task_to_delete_order = request.GET.get('order')
    Tasks.objects.filter(order=task_to_delete_order).delete()
    tasks = Tasks.objects.filter(order__gt=task_to_delete_order)
    for task in tasks:
        task.order -= 1
        task.save()
    return redirect(index)
