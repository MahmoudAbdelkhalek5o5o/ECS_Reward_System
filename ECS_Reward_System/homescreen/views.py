import datetime
from audioop import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from Users.models import announcements,Role , User , UserRegisterationRequests
from activities.models import ActivityCategory , Activity , ActivityRequest , ActivitySuggestion ,Points

from Rewards.models import budget , Vendors , Vouchers , Redemption_Request , Suggest_Reward
from django import forms
import pytz


# Create your views here.

def index(request):
    #Resetting the budget at the begining of the year
    if (datetime.datetime.now().month == 1 and datetime.datetime.now().day == 1):
        budget.objects.filter(year = int(datetime.datetime.now().year), is_active = True).update(is_active = False)
        
        

    Announcements = announcements.objects.filter().all().order_by('-StartDate')
    Announcements = announcements.objects.filter().all().order_by('StartDate')
    utc=pytz.UTC
    now = utc.localize(datetime.datetime.now())
   
    for announcement in Announcements:
        if now > announcement.EndDate:
            announcements.objects.filter(pk = announcement.id).update(is_archived = True)
       
        
    #Checking if user was authenticated.

    if request.user.is_authenticated and request.user.role == "Role.A":
        return render(request,'homescreen/index.html',{
             "add_notification": Add_Notification_form(),
             "announcements": Announcements
         })
    elif request.user.is_authenticated and budget.objects.filter(year = int(datetime.datetime.now().year), is_active = True):
        egp = budget.objects.filter(year = int(datetime.datetime.now().year), is_active = True)[0]
        amount = request.user.points//egp.point
        print(egp.point)
        return render(request,'homescreen/index.html',{
             "announcements": Announcements,
             "user":request.user,
             "amount":amount
         })
    elif request.user.is_authenticated and not budget.objects.filter(year = int(datetime.datetime.now().year), is_active = True):
        return render(request,'homescreen/index.html',{
             "announcements": Announcements,
             "user":request.user,
             
         })
    
        
         
     #if the user was not authenticated then they should be redirected back to the login page
    else:
        return redirect('login')
    
    
    
def announcement_view(request,anouncement_id):
    #grab the announcement by its Id
    announcemnt = announcements.objects.get(pk = anouncement_id)
    

    #send the announcement to the announcement view page
    return render(request,"homescreen/announcement_view.html",{
        "announcement":announcemnt
    })
    
def delete_announcements_view(request,anouncement_id):
    if request.user.role == "Role.A":
        #grab the announcement by the id
        announcement = announcements.objects.get(pk = anouncement_id)
        #delete announcement
        announcement.delete()
        return redirect('users-home')


class Add_Notification_form(forms.Form):
    Notification= forms.CharField(label="Add Announcements" ,widget= forms.Textarea(attrs={
        "class": "form-control",
        "id":"exampleFormControlTextarea1",
        "placeholder": "Announcement",
        "required" : "True"
    }))
    Notification_EndDate= forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control', 'style': 'width:350px','required':'True'}), required= True)
def add_notifications(request):
    #checks if user is authenticated
    if request.user.is_authenticated and request.user.role=="Role.A":
        if request.method == "POST":
            form= Add_Notification_form(request.POST)
            #checks if the fields are not empty
            if form.is_valid():
                #gras the data in the input fields
                Announcemnt_EndDate= request.POST["Notification_EndDate"]
                Notification=request.POST["Notification"]
                #save those data entries in the database
                announcemnt=announcements(PostText = Notification,EndDate = Announcemnt_EndDate,creator = request.user)
                announcemnt.save()
            
    return redirect("users-home")
    
    
def view_archive(request, model_name):
    models_data = ['Users', 'Announcemnts', 'Vendors', 'Redemption Requests', 'Reward Suggestions', 'Categories', 
    'Activities', 'Activity Requests', 'Activity Suggestions']
    if request.user.is_authenticated:
        if request.user.role == "Role.A":
            msg=''
            match model_name:
                case 'Users':
                    data = User.objects.filter(is_archived = True).all()
                    if not data:
                        msg = "No Archived Users!"
                    return render (request,"homescreen/archive.html",{
                        'Users':data,
                        'data':models_data,
                        'no_users':msg
                    })
                
                case 'Announcemnts':
                    data = announcements.objects.filter(is_archived = True).all().select_related('creator')
                    if not data:
                        msg = "No Archived Announcements!"
                    return render (request,"homescreen/archive.html",{
                        'announcemnts':data,
                        'data':models_data,
                        'no_announcemnts':msg
                    })
                case 'Vendors':
                    data = Vendors.objects.filter(is_archived = True).all()
                    if not data:
                        msg = "No Archived Vendors!"
                    return render (request,"homescreen/archive.html",{
                        'Vendors':data,
                        'data':models_data,
                        'no_vendors':msg
                    })
                case 'Vouchers':
                    data = Vouchers.objects.filter(is_archived = True).all()
                    if not data:
                        msg = "No Archived Vouchers!"
                    return render (request,"homescreen/archive.html",{
                        'Vouchers':data,
                        'data':models_data,
                        'no_vouchers':msg
                    })
                case 'Redemption Requests':
                    data = Redemption_Request.objects.filter(is_archived = True).all().select_related('employee','voucher', 'approved_by')
                    if not data:
                        msg = "No Archived Redemption Requests!"
                    return render (request,"homescreen/archive.html",{
                        'Redemption_requests':data,
                        'data':models_data,
                        'no_redemption_requests':msg
                    })
                case 'Reward Suggestions':
                    data = Suggest_Reward.objects.filter(is_archived = True).all()
                    if not data:
                        msg = "No Archived Reward Suggestions!"
                    return render (request,"homescreen/archive.html",{
                        'Suggest_Rewards':data,
                        'data':models_data,
                        'no_reward_suggestions':msg
                    })
                case 'Categories':
                    data = ActivityCategory.objects.filter(is_archived = True).all().select_related('owner')
                    if not data:
                        msg = "No Archived Categories!"
                    return render (request,"homescreen/archive.html",{
                        'Categories':data,
                        'data':models_data,
                        'no_categories':msg
                    })
                case 'Activities':
                    data = Activity.objects.filter(is_archived = True).all().select_related('category')
                    if not data:
                        msg = "No Archived Activities!"
                    return render (request,"homescreen/archive.html",{
                        'Activities':data,
                        'data':models_data,
                        'no_activities':msg
                    })
                case 'Activity Requests':
                    data = ActivityRequest.objects.filter(is_archived = True).all().select_related('emp','activity','category')
                    if not data:
                        msg = "No Archived Activity Requests!"
                    return render (request,"homescreen/archive.html",{
                        'ActivityRequests':data,
                        'data':models_data,
                        'no_activity_requests':msg
                    })
                case 'Activity Suggestions':
                    data = ActivitySuggestion.objects.filter(is_archived = True).all().select_related('category')
                    if not data:
                        msg = "No Archived Activity Suggestions!"
                    return render (request,"homescreen/archive.html",{
                        'ActivitySuggestions':data,
                        'data':models_data,
                        'no_activity_suggestions':msg
                    })
        else:
            return redirect('users-home')
    else:
        return redirect('login')
