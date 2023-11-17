from django import forms
from crm.models import Employees
from django.contrib.auth.models import User


# class EmployeForm(forms.Form):
#   name=forms.CharField()
#   department=forms.CharField()
#   salary=forms.IntegerField()
#   email=forms.EmailField()
#   age=forms.IntegerField()
#   contact=forms.IntegerField()

 #or using model form(it became easy than normal form)

class EmployeeModelForm(forms.ModelForm):
  class Meta:
    model=Employees
    fields="__all__"
    widgets={           #for styling textbox
      "name":forms.TextInput(attrs={"class":"form-control"}),
      "department":forms.TextInput(attrs={"class":"form-control"}),
      "salary":forms.NumberInput(attrs={"class":"form-control"}),
      "email":forms.EmailInput(attrs={"class":"form-control"}),
      "age":forms.NumberInput(attrs={"class":"form-control"}),
      "contact":forms.Textarea(attrs={"class":"form-control","row":5}),
      "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})





    }

 #for register form

class RegisterModelForm(forms.ModelForm):
  class Meta:
    model=User
    fields=["username","email","password"]  

#for login form(normalform)
class LoginForm(forms.Form):
  username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","row":5}))
  password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","row":5}))

    