from django.shortcuts import render,redirect#delete kazhinne list ilakke povanameghil
from django.views.generic import View
from crm.forms import EmployeeModelForm,RegisterModelForm,LoginForm
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

#decorator(login cheyyate vakki ulla pgil poyaal tiriche loginil tanne varutaan)
def signin_required(fn):
     def wrapper(request,*args,**kwargs):
       if not request.user.is_authenticated:
          messages.error(request,"invalid session")
          return redirect('signin')
       else:
          return fn(request,*args,**kwargs)
     return wrapper
       



# Create employee- localhost:8000/employees/add
@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
   
    def get(self,request,*args,**kwargs):
         form=EmployeeModelForm()
         return render(request,"employee_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
         form=EmployeeModelForm(request.POST,files=request.FILES)
         if form.is_valid():
              form.save() #we can use this instead of orm query (bcoz modelform use)
              #orm query for create
          # Employees.objects.create(**form.cleaned_data) #dictionary ne fetch cheyyan vendiyane **
              messages.success(request,"succefully employee created")
              return render(request,"employee_add.html",{"form":form})
         else:
             messages.error(request,"employee added failed")
             return render(request,"employee_add.html",{"form":form})

#list employee-localhost:8000/employees/list
@method_decorator(signin_required,name="dispatch")

class EmployeeListView(View):
     def get(self,request,*args,**kwargs):
           qs=Employees.objects.all()
           departments=Employees.objects.all().values_list("department",flat=True).distinct()
           print(departments)
           #list employee-localhost:8000/employees/list?department=it
           if "department"in request.GET:
                dept=request.GET.get("department")
                qs=qs.filter(department__iexact=dept)

           return render(request,"emp_list.html",{"data":qs,"department":departments})
         
     def post(self,request,*args,**kwargs):
          name=request.POST.get("box")
          qs=Employees.objects.filter(name__icontains=name)#eetelum letter undaghilum search cheyyumbool kittum
          return render(request,"emp_list.html",{"data":qs})


#detail view{id}or{pk} localhost:8000/employees/{id}
@method_decorator(signin_required,name="dispatch")

class EmployeeDetailView(View):
          def get(self,request,*args,**kwargs):
               #urlile id varan
               print(kwargs) #{"pk":6}
               id=kwargs.get("pk") #pk ne matram edukkan
               # orm query for getting id(for database)
               qs=Employees.objects.get(id=id)

               return render(request,"emp_detail.html",{"data":qs})

#delete -localhost:8000/employees/{id}/remove 
@method_decorator(signin_required,name="dispatch")

class EmployeeDeleteView(View):
          def get(self,request,*args,**kwargs):
      
               id=kwargs.get("pk") 
               Employees.objects.get(id=id).delete()
               messages.success(request,"succefully employee has been deleted")


               return redirect("emp-list")
          
#edit-localhost:8000/employees/{id}/edit
@method_decorator(signin_required,name="dispatch")

class EmployeeEditView(View):
          def get(self,request,*args,**kwargs):
                id=kwargs.get("pk")
                obj=Employees.objects.get(id=id) #edit cheyyumbool same data varan changeil
                form=EmployeeModelForm(instance=obj)
                return render(request,"emp_edit.html",{"form":form})
          
          def post(self,request,*args,**kwargs):
            id=kwargs.get("pk")
            obj=Employees.objects.get(id=id)
            form=EmployeeModelForm(request.POST,files=request.FILES,instance=obj)
            if form.is_valid():
              form.save() 
              messages.success(request,"employee has been added edited")

             
          #     return redirect("emp-list")-list pgilakke povan
              return redirect("emp-detail",pk=id) #detail pg ilakke povan
            else:
             messages.error(request,"employee edited failed")

             return redirect(request,"emp_edit.html",{"form":form})
      
#register-localhost:8000/signup/
class SignUpView(View):
     def get(self,request,*args,**kwargs):
          form=RegisterModelForm()
          return render(request,"register.html",{"form":form})
     
     def post(self,request,*args,**kwargs):
          form=RegisterModelForm(request.POST)
          if form.is_valid():
               User.objects.create_user(**form.cleaned_data)#password ne encrypte cheyyan
               print("saved")
               messages.success(request,"account has been created")
               return render(request,"register.html",{"form":form})
          else:
              print("failed")
              messages.error(request,"something went wrong")

              return render(request,"register.html",{"form":form})

#login view
class SignInView(View):
     def get(self,request,*args,**kwargs):
          form=LoginForm()
          return render(request,"login.html",{"form":form})
     
     def post(self,request,*args,**kwargs):
          form=LoginForm(request.POST)
          if form.is_valid():
               #1-extract data,check data
               user_name=form.cleaned_data.get("username")
               pwd=form.cleaned_data.get("password") 
               print(user_name,pwd)  
               #2- section start
               user_obj=authenticate(request,username=user_name,password=pwd)
               if user_obj:
                    print("valid credentils")
                    login(request,user_obj)
                    #3-store 
                    login(request,user_obj)
                    return redirect("emp-list")
               messages.error(request,"invalid credentils")
               return render(request,"login.html",{"form":form})
          

#logout
@method_decorator(signin_required,name="dispatch")

class SignOutView(View):
     def get(self,request,*args,**kwargs):
      logout(request)
      return redirect("signin")










