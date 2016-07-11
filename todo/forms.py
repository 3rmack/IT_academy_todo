from django import forms


class TaskForm(forms.Form):
    task = forms.CharField(max_length=100, required=True, min_length=1)


# class TaskEditForm(forms.Form):
#     # task = forms.CharField(max_length=100)
#     status = forms.BooleanField()
