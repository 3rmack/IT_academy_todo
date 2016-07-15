# coding: UTF-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import Tasks
from forms import TaskForm


def index(request):  # главная страница со списком задач
    tasks = Tasks.objects.filter().order_by('order')  # получение всех задач из базы отсортированных по order
    context = {'tasks': tasks}
    return render(request, 'index.html', context)


def add_task(request):  # добавление задачи
    if request.method == 'POST':
        raw_data = TaskForm(request.POST)
        if raw_data.is_valid():
            data = raw_data.cleaned_data

            if Tasks.objects.filter().order_by('order').last():  # проверка на наличие в базе задач
                last_task = Tasks.objects.filter().order_by('order').last()  # если есть - получаем последнюю задачу, нужна для создания новой задачи с увеличенным order на 1
                Tasks.objects.create(order=last_task.order+1, **data)  # увеличиваем order последней задачи на 1 и записываем в базу новую задачу
            else:  # если база пуста, создаем задачу с order = 1, т.е. первая в списке
                Tasks.objects.create(order=1, **data)

            return redirect(index)
        else:
            context = {'message': 'Task name cannot be empty'}
            return render(request, 'error.html', context)
    else:
        context = {'task_add_form': TaskForm()}
        return render(request, 'task_add_form.html', context)


def updown(request):  # перемещение залачи вверх\вниз по списку
    task_to_modify = request.GET  # в линке на html странице в GET параметрах указан type перемещения (up или down) и order задачи которую нужно переместить
    try:
        if task_to_modify['type'] == 'up':  # перемещием задачи вверх
            task_to_move_up = Tasks.objects.get(order=task_to_modify['order'])  # получение задачи, которую нужно переместить
            if task_to_move_up.order == 1:  # если order перемещаемой задачи равен 1 (т.е. она первая) - игнорируется и отрисовывается главная страница
                return redirect(index)
            else:  # в противном случае запуск перемещения
                task_to_move_down = Tasks.objects.get(order=int(task_to_modify['order'])-1)  # получение задачи, находящейся над перемещаемой
                task_to_move_up.order = task_to_move_down.order  # изменение order перемещаемой задачи на order задачи, находящейся выше
                task_to_move_down.order = task_to_modify['order']  # изменение order задачи находящейся выше на order перемещаемой
                task_to_move_up.save()
                task_to_move_down.save()
                return redirect(index)
        elif task_to_modify['type'] == 'down':  # перемещием задачи вниз
            last_task = Tasks.objects.filter().order_by('order').last()  # получение последней по списку задачи
            task_to_move_down = Tasks.objects.get(order=task_to_modify['order'])  # получением перемещаемой вниз задачи
            if task_to_move_down.order == last_task.order:  # если order последней и перемещаемой задачи равны (т.е. перемещаемая задача - последняя)
                return redirect(index)  # игнорирование и перенаправление на главную страницу
            else:  # в противном случае запуск перемещения
                task_to_move_up = Tasks.objects.get(order=int(task_to_modify['order'])+1)  # получение задачи, которую нужно переместить вверх
                task_to_move_up.order = task_to_move_down.order  # изменение order перемещаемой задачи на order задачи, находящейся выше
                task_to_move_down.order = int(task_to_modify['order']) + 1  # увеличение order перемещаемое вниз задачи
                task_to_move_up.save()
                task_to_move_down.save()
                return redirect(index)
        else:  # ловим обращения с некорректным параметром type
            context = {'message': 'Incorrect \'type\' parameter'}
            return render(request, 'error.html', context)
    except KeyError:  # ловим обращения с пустыми type или order
        context = {'message': 'No \'type\' or \'order\' parameter'}
        return render(request, 'error.html', context)
    except ValueError:   # ловим обращения с некорректным параметром order
        context = {'message': 'Incorrect \'order\' parameter'}
        return render(request, 'error.html', context)
    except Tasks.DoesNotExist:  # ловим обращения к базе с несуществующими order
            context = {'message': 'No task with such \'order\''}
            return render(request, 'error.html', context)


def edit(request):  # редактирование задачи
    if request.method == 'POST':
        task_to_modify = request.POST
        task = Tasks.objects.get(id=task_to_modify['id'])
        if task_to_modify['task']:  # если имя задачи не пустое
            task.task = task_to_modify['task']  # изменение имени задачи на новое
        else:  # в противном случае выводим сообщение об ошибке
            context = {'message': 'Task name cannot be empty'}
            return render(request, 'error.html', context)
        if 'status' in task_to_modify:  # если checkbox "Finished" нажат, в дикте появляется кдюч 'status', проверка на наличие данного ключа в дикте
            task.status = True  # если 'status' присутствует, значит пользователь указал, что задача выполнена - измение статуса в базе
        else:  # в противном случае меняем status на False, т.е. не выполнено
            task.status = False
        task.save()
        return redirect(index)
    else:
        task_to_modify_id = request.GET.get('id')  # в GET запросе получение id изменяемой задачи
        try:
            task_to_modify = Tasks.objects.get(id=int(task_to_modify_id))  # получение изменяемой задачи
            context = {'task': task_to_modify}
            return render(request, 'task_edit_form.html', context)
        except Tasks.DoesNotExist:  # ловим обращения к базе с несуществующими id
            context = {'message': 'No task with such id'}
            return render(request, 'error.html', context)
        except ValueError:  # ловим обращения с пустыми или неправильными id
            context = {'message': 'Unable to retrieve task with empty or incorrect id'}
            return render(request, 'error.html', context)
        except TypeError:  # ловим обращения к edit без GET параметра id
            context = {'message': 'Unable to retrieve task with empty id'}
            return render(request, 'error.html', context)


def delete(request):  # удаление задачи
    task_to_delete_order = request.GET.get('order')  # получение из GET запроса order удаляемой задачи
    Tasks.objects.filter(order=task_to_delete_order).delete()  # удаление задачи
    # т.к. из базы удалена запись, то нарушается последовательность order, нужно сдвинуть order всех нижестоящих задач на 1 вверх
    tasks = Tasks.objects.filter(order__gt=task_to_delete_order)  # получение всех нижестоящих задач
    for task in tasks:
        task.order -= 1  # сдвиг order
        task.save()
    return redirect(index)
