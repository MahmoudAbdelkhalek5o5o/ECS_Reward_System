from copyreg import constructor
import email
from msilib.schema import Error
from tkinter import EXCEPTION
from venv import create
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import  User, Role , UserRegisterationRequests
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, change_password_form, UpdateUserForm , UpdateUserrequestForm , SignupForm
from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import default_token_generator 
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UpdateUserForm
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    
    
    
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


def validate_domain(data):
    if '@' in data:
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        if len(data.split('@')[0])<3:
            return False
        if domain == ecsDomain:
            return True
        return False
    return False

def validate_password(password):
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) 
        and any(x.isdigit() for x in password)):
            return True
        return False

def get_error_messages_register(user):
    error_messages = {}
    if len(user['username'])<3 or len(user['username'])>20:
        error_messages['username']="Username length must be greater than 3 and less than 20"
    if len(user['first_name'])<3 or len(user['first_name'])>20:
        error_messages['first_name']="First name length must be greater than 3 and less than 20"
    if len(user['last_name'])<3 or len(user['last_name'])>20:
        error_messages['last_name']="Last name length must be greater than 3 and less than 20"
    if not validate_domain(user['email']):
        error_messages['email']="Please enter an Email Address with ecs domain domain"
    if not validate_password(user['password']) or len(user['password'])<8 or len(user['password'])>16:
        error_messages['password'] = "Password must contains digits, uppercase and lowercase letter with length between 8 and 16"
    if user["password"] != user["confirmation"]:
        error_messages['confirmation']="Passwords must match."
    if user['number_0'] == '':
        error_messages['number']="Country Code is required"
    if user['number_1'] == '':
        error_messages['number']="Phone number is required"
    if user['emp_id'] == '':
        error_messages['emp_id']="ID is required"
    # if not 'img' in user or user['img'] == '':
    #     error_messages.append("Profile Picture is required")
    return error_messages
# Create your views here.



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        user = request.POST.dict()
        user.pop('csrfmiddlewaretoken')
        if 'img' in request.FILES:
            user["img"]=request.FILES["img"]
        else:
            user.pop('img')
        print(user)
        user['phone_number'] = user['number_0'] + " " + user["number_1"]
        # form constraints
        error_messages = get_error_messages_register(user)
        user["role"] = "Role.E"
        user.pop('number_0')
        user.pop('number_1')
        user.pop('confirmation')
        # phone number validation error
        if not form.is_valid():
            error_messages['number']="Enter a valid phone number (e.g. (20) 01000123456) or a number with an international call prefix."
            return render(request, "accounts/sign_up.html", {
                "error_messages": error_messages,
                'form':form
            })
        # form validation errors
        else:
            if not error_messages == {}:
                print(error_messages)
                return render(request, "accounts/sign_up.html", {
                "error_messages": error_messages,
                'form':form,
            })
        # Attempt to create new user
            try:
                # database constraints errors
                
                # username already exists
                if User.objects.filter(username=user["username"], is_archived=False).exists():
                    error_messages['username'] = "Username Already Exists"
                    return render(request, "accounts/sign_up.html", {
                        "error_messages": error_messages,
                        "message": "Username Already Exists",
                        'form':form
                    })
                # ID already exists
                if User.objects.filter(emp_id=user["emp_id"]).exists():
                    error_messages['emp_id'] = "ID Already Exists"
                    return render(request, "accounts/sign_up.html", {
                        "error_messages": error_messages,
                        "message": "ID Already Exists",
                        'form':form
                    })
                # email already exists
                if User.objects.filter(email=user["email"]).exists():
                    error_messages['email'] = "Email Already Exists"
                    return render(request, "accounts/sign_up.html", {
                        "error_messages": error_messages,
                        "message": "Email Already Exists",
                        'form':form
                    })
                # phone number already exists
                if User.objects.filter(phone_number=user["phone_number"]).exists():
                    error_messages['number'] = "Phone number Already Exists"
                    return render(request, "accounts/sign_up.html", {
                        "error_messages": error_messages,
                        "message": "Phone number Already Exists",
                        'form':form
                    })
                UserRegisterationRequests.objects.create(**user)
                # user request created successfully
                return render(request, "accounts/sign_up.html", {
                    "success_message": "Registeration request has been submitted and will be reviewed by HR soon",
                    'form':RegisterForm()
                    })
            except IntegrityError:
                # username already exists
                
                if UserRegisterationRequests.objects.filter(emp_id=request.POST["emp_id"], is_archived=False).exists():
                    return render(request, "accounts/sign_up.html", {
                        "message": "Your request is pending",
                        'form':form
                    })
    else:
        return render(request, "accounts/sign_up.html", {'form':RegisterForm()
        })


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":

        # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
        # Check if authentication successful
            if user is not None:
                login(request, user)
                return redirect("users-home")
        #if authentication is not succesful an error message is displayed
            else:
                return render(request, "accounts/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "accounts/login.html")
    else:
         logout(request)
         return redirect('login')
    


    
def logout_view(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if request.user.is_authenticated:
        form = change_password_form()

        if request.method == 'POST':
            form = change_password_form(request.POST)
            if form.is_valid():
                password = request.POST["password"]
                user = authenticate(username=request.user.username, password=password) #authenticates if the old password entered is correct
                if user is not None:
                    if not form.validate_password():
                        return render(request,'accounts/change.html', {
                            'form': form,
                            'message':"Password must contains digits, uppercase and lowercase letter" # if confirmation and new password are not equivelant generate a message to enter passwords that match
                    })
                    new_password=request.POST["New_password"] #if old password is correct the user should enter the new password
                    confirmation = request.POST["confirmation"] #the user should confirm the new password entered and write it again
                    if new_password == confirmation:
                        create_password = make_password(new_password) # if the confirmed password entered is the same as the new password update the password
                        User.objects.filter(pk = request.user.emp_id).update(password = create_password)
                        #logout(request,request.user)
                        return redirect('login') #redirects the user to the login page to login with the new password
                    else:
                        return render(request,'accounts/change.html', {
                            'form': form,
                            'message':"passwords don't match" # if confirmation and new password are not equivelant generate a message to enter passwords that match
                        })

                else:
                
                    return render(request,'accounts/change.html', {
                        'form': form,
                        'message':"Old password is incorrect" #if old password is incorrect generate a message to tell the user to enter the correct old password

        })
        
  
        else:
            print(8)
            return render(request,'accounts/change.html', {
                    'form': form, 
                    
        })
    else:
        return redirect("login")





def userEdit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST , request.FILES, instance=request.user)
            
            if user_form.is_valid():
              
                if not user_form.validate_phone_number() and  request.user.phone_number == user_form.validate_phone_number():
                 
                    return render(request, 'accounts/useredit_form.html', {
                        'user_form': user_form,
                        'message':'Phone number already exists'
                    }
                    )
                   
                if not user_form.clean_username():
                     return render(request, 'accounts/useredit_form.html', {
                        'user_form': user_form,
                           'message':'Username already exists'
                    }
                           )
                    
                    
                    
             
                else:   
                    user_form.save('user_form.is_valid()')
                
    
                    messages.success(request, 'Your profile is updated successfully')
                    return redirect(to='users-home')
            else:
                return render(request, 'accounts/useredit_form.html', {
                        'user_form': user_form,
                           'message':'Username or mobile already exists!'
                    }
                           )
        else:
            user_form = UpdateUserForm(instance=request.user)
       

        return render(request, 'accounts/useredit_form.html', {'user_form': user_form})
    else:
        return redirect("login")

def Admin_View_register_request(request):
    if request.user.is_authenticated and request.user.role == "Role.A":
        register_requests = UserRegisterationRequests.objects.filter().all()
        return render(request,"accounts/Admin_view_requests.html",{"register_requests":register_requests})
    else:
        return redirect("login")


def Admin_accept_register(request,request_id):
    if request.user.role == "Role.A":
        request_register = UserRegisterationRequests.objects.get(pk = request_id)
        if request.method == "POST":
          
            user =  User.objects.create_user(username = request_register.username , 
                                             emp_id = request_register.emp_id,
                                            
                                            password = request_register.password ,
                                            phone_number = request_register.phone_number,
                                            role = request_register.role,
                                            img = request_register.img,
                                            email = request_register.email,
                                            first_name = request_register.first_name,
                                            last_name = request_register.last_name,
                                            
                                            )
            user.save()
            request_register.delete()
            send_mail(
                        'Register Request',
                        'Your register request have been accepted please follow this link to log in 127.0.0.1/authentication/',
                        'muhammad.mazen4@gmail.com.com',
                        ['youssef.ismail@ecs-co.com'],
                        fail_silently=False,
                                            )
            return redirect("register_request")
            
        else:
            return render(request,"accounts/Admin_view_requests.html")
    else:
        return(redirect("login"))


def Admin_reject_register(request,request_id):
    if request.user.role == "Role.A":
        request_register = UserRegisterationRequests.objects.get(pk = request_id)
        if request.method == "POST":
           
            request_register.delete()
            send_mail(
                        'Register Request',
                        'Your register request have been rejected if you feel like this was a mistake please contact the HR and re register br\ regards,Admin',
                        'muhammad.mazen4@gmail.com.com',
                        ['youssef.ismail@ecs-co.com'],
                        fail_silently=False,
                                            )
            return redirect("register_request")
        else:
            return render(request,"accounts/Admin_view_requests.html")
    else:
        return(redirect("login"))
            
            
def view_profile(request,emp_id):
    register_request = UserRegisterationRequests.objects.get(pk = emp_id)
    return render(request,"accounts/profile_view.html",{
        "register_request":register_request
})
            
    
def profiles(request):
    if request.user.role == "Role.A":
        users = User.objects.filter(is_archived = False)
        profiles = []
        for user in users:
            if not request.user == user:
                profiles.append(user)
                
        return render(request,"accounts/users_view.html",{
            "profiles":profiles
        }) 
    

def edit_register_request(request,emp_id):
    if request.user.role == "Role.A":
      
        emp = UserRegisterationRequests.objects.get(pk = emp_id)
        if request.method == 'POST':
            user_form = UpdateUserrequestForm(request.POST , request.FILES, instance=emp)
            
            if user_form.is_valid():
              
                if not user_form.validate_phone_number() and  emp.phone_number == user_form.validate_phone_number():
                 
                    return render(request, 'accounts/edit_register_request.html', {
                        'user_form': user_form,
                        'message':'Phone number already exists'
                    }
                    )
                   
                if not user_form.clean_username():
                     return render(request, 'accounts/edit_register_request.html', {
                        'user_form': user_form,
                           'message':'Username already exists'
                    }
                           )
                    
                    
                    
             
                else:   
                    User.object.create_user(pk = emp_id , username = request.POST['username'], first_name = request.POST['first_name'],
                                            last_name = request.POST['last_name'], email = request.POST['email'],
                                            phone_number = request.POST['phone_number'], role = request.POST['role'])
                    emp.delete()
                
    
                    messages.success(request, 'Your profile is updated successfully')
                    return redirect(to='users-home')
            else:
                return render(request, 'accounts/edit_register_request.html', {
                        'user_form': user_form,
                           'message':'Username or mobile already exists!'
                    }
                           )
        else:
            user_form = UpdateUserrequestForm(instance=emp)
       

        return render(request, 'accounts/edit_register_request.html', {'user_form': user_form})
    else:
        return redirect("login")
        
def admin_create_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST,request.FILES)
        user = request.POST.dict()
        user.pop('csrfmiddlewaretoken')
        if 'img' in request.FILES:
            user["img"]=request.FILES["img"]
        else:
            user.pop('img')
        user['phone_number'] = user['number_0'] + " " + user["number_1"]
        # form constraints
        error_messages = get_error_messages_register(user)
        user.pop('number_0')
        user.pop('number_1')
        user.pop('confirmation')
        # phone number validation error
        if not form.is_valid():
            error_messages['number']="Enter a valid phone number (e.g. (20) 01000123456) or a number with an international call prefix."
            return render(request, "accounts/admin_create_user.html", {
                "error_messages": error_messages,
                'form':form
            })
        # form validation errors
        else:
            if not error_messages == {}:
                return render(request, "accounts/admin_create_user.html", {
                "error_messages": error_messages,
                'form':form
            })
        # Attempt to create new user
            try:
                # database constraints errors
                
                # username already exists
                if User.objects.filter(username=user["username"], is_archived=False).exists():
                    error_messages['username'] = "Username Already Exists"
                    return render(request, "accounts/admin_create_user.html", {
                        "error_messages": error_messages,
                        "message": "Username Already Exists",
                        'form':form
                    })
                # ID already exists
                if User.objects.filter(emp_id=user["emp_id"]).exists():
                    error_messages['emp_id'] = "ID Already Exists"
                    return render(request, "accounts/admin_create_user.html", {
                        "error_messages": error_messages,
                        "message": "ID Already Exists",
                        'form':form
                    })
                # email already exists
                if User.objects.filter(email=user["email"]).exists():
                    error_messages['email'] = "Email Already Exists"
                    return render(request, "accounts/admin_create_user.html", {
                        "error_messages": error_messages,
                        "message": "Email Already Exists",
                        'form':form
                    })
                # phone number already exists
                if User.objects.filter(phone_number=user["phone_number"]).exists():
                    error_messages['number'] = "Phone number Already Exists"
                    return render(request, "accounts/admin_create_user.html", {
                        "error_messages": error_messages,
                        "message": "Phone number Already Exists",
                        'form':form
                    })
                User.objects.create_user(**user)
                # user request created successfully
                return render(request, "accounts/admin_create_user.html", {
                    "success_message": "User Created Successfully",
                    'form':SignupForm()
                    })
            except IntegrityError:
                # username already exists
                
                if UserRegisterationRequests.objects.filter(emp_id=request.POST["emp_id"], is_archived=False).exists():
                    return render(request, "accounts/admin_create_user.html", {
                        "message": "Your request is pending",
                        'form':form
                    })
    else:
        return render(request, "accounts/admin_create_user.html", {'form':SignupForm()})