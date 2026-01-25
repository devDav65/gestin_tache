from django import forms
from .models import Task



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titre', 'description']

# class SiginUp(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username','email','password1','password2']
