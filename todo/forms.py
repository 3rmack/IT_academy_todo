from django import forms


class TaskForm(forms.Form):
    task = forms.CharField(max_length=100)
    # status = forms.BooleanField()
    # order = forms.IntegerField()
