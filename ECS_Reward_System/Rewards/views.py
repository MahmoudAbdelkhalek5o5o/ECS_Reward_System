from django.shortcuts import render,redirect
from .models import Vendors, Vouchers , Suggest_Reward,Redemption_Request , budget
from Users.models import User , announcements
from activities.models import Points
from django.core.mail import send_mail
import pytz
from datetime import datetime,date,timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

# Create your views here.
def is_expired(end_date):
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    if now >= end_date:
        return True
    else:
        return False

def create_vendor(request):
    if request.user.role == "Role.A":
        if request.method == "POST":
            name = request.POST["name"]
            start_date = request.POST["start_date"]
          
            end_date = request.POST["end_date"]
            Logo = request.FILES["Logo"]
            if Vendors.objects.filter(name=request.POST["name"]).exists():
                return render(request,"rewards/create_vendor.html",{
                "warning_message":"Vendor Already Exists try adding vouchers to that Vendor"
            })
            else:
                if end_date:
                    Vendors.objects.create(name = name , end_date = end_date , img = Logo , start_date = start_date , creator = request.user)
                else:
                    Vendors.objects.create(name = name  , img = Logo , start_date = start_date , creator = request.user)
                    
                announcements.objects.create(creator = request.user , PostText = f"A new vendor {name} is added!!",EndDate = datetime.now() + timedelta(days=30))
                return render(request,"rewards/create_vendor.html",{
                "message":"Vendor successfuly added"
                })
        else:
            return render(request,"rewards/create_vendor.html")
    else:
        return redirect("login")
    
def view_vendors(request):
    if request.user.is_authenticated:
        all_vendors = Vendors.objects.filter().all()
        vendors = []
        utc=pytz.UTC
        now = utc.localize(datetime.now())
        for vendor in all_vendors:
            if vendor.start_date <= now:
                vendors.append(vendor)
        return render(request,"rewards/vendors.html",{
            "vendors": vendors
})
def vendor_view(request,vendor_id):
    vendor = Vendors.objects.get(pk = vendor_id)
    vouchers = Vouchers.objects.filter(vendor = vendor).all()
    return render(request,"rewards/vendor.html",{
        "vendor":vendor,
        "vouchers":vouchers
})


def add_new_reward(request):
    if request.user.role == "Role.A":
        if request.method == "POST":
            vendor = request.POST["name"]
            getvendor = Vendors.objects.get(name = vendor)
            start_date = request.POST["start_date"]
           
            end_date = request.POST["end_date"]
            points = request.POST["points_equivalent"]
            if end_date:
                Vouchers.objects.create(vendor = getvendor, end_date = end_date, points_equivalent=points , start_date = start_date , creator = request.user)
            else:
                Vouchers.objects.create(vendor = getvendor, points_equivalent=points , start_date = start_date , creator = request.user)
            announcements.objects.create(creator = request.user , PostText = f"A new Reward from {vendor} is added!!",EndDate = end_date)
            return render(request,"rewards/create_reward.html",{
                "message":"Reward Successfuly Added"
                })

        else:
            return render(request,"rewards/create_reward.html")
    else:
        return redirect("login")
def suggest_rewards(request):
    if request.method== "POST":
        if request.user.role == "Role.M" or request.user.role == "Role.E" :
            getvendorname= request.POST['vendor']
            getwebsite= request.POST['website']
            getreason= request.POST['reason']
            Suggest_Reward.objects.create(vendor = getvendorname , website=getwebsite, reason=getreason)
            
            return render(request,"rewards/suggest_rewards.html", {
                'message': "Vendor suggestion has been successfully submitted"
            })
    
    else:
        
        
        return render(request,"rewards/suggest_rewards.html")
    
def redemption_request(request,voucher_id):
    if not request.user.role == "Role.A":
        voucher = Vouchers.objects.get(pk = voucher_id)
        if request.method == "POST":
            points_equivalent = voucher.points_equivalent
            if request.user.points >= voucher.points_equivalent:
                points_needed = []
                points = Points.objects.filter(employee = request.user,is_used = False).order_by('end_date')
                for point in points:
                    if is_expired(point.end_date) == False:
                        points_needed.append(point)
                for point in points_needed:
                    acquired = 0
                    if acquired < points_equivalent:
                        acquired = acquired + point.points
                        if acquired > points_equivalent:
                        
                            Points.objects.filter(pk = point.id).update(points = acquired - points_equivalent)
                            break
                        else:
                            Points.objects.filter(pk = point.id).update(is_used = True)
               
                User.objects.filter(username = request.user.username).update(points = request.user.points - points_equivalent)       
                Redemption_Request.objects.create(voucher = voucher,employee = request.user)
                return redirect("users-home")
            else:
                return HttpResponseRedirect(reverse("vendor", args = (voucher_id,)))
        

 

def admin_view_redemption_requests(request):
    if request.user.is_authenticated and request.user.role == "Role.A":
        redemption_requests = Redemption_Request.objects.filter(status='Status.P')
        return render(request,"rewards/admin_view_redemption_requests.html",{
            "redemption_requests":redemption_requests})
    else:
        return redirect("login")

def redemption_request_view(request,redemption_request_id):
    redemption_request = Redemption_Request.objects.get(pk = redemption_request_id)
    return render(request,"rewards/admin_redemption_request_view.html",{"redemption_request":redemption_request}) 

def decline_redemption(request,request_id):
    if request.user.role == "Role.A":
        redemption_request = Redemption_Request.objects.get(pk = request_id)
        user = redemption_request.employee
        if request.method == "POST":
            
            Redemption_Request.objects.filter(pk = request_id).update(status='Status.D')
            User.objects.filter(username = user.username).update(points = user.points + redemption_request.voucher.points_equivalent)
            send_mail(
                    'Redemption Request',
                    'Your redemption request has been rejected',
                    'muhammad.mazen4@gmail.com.com',
                    [f'{Redemption_Request.objects.get(pk = request_id).employee.email}'],
                    fail_silently=False,)
            return redirect("admin_view_redemption_requests")
        else:
            return redirect("users-home")
    else:
        return(redirect("login"))  
def accept_redemption(request , request_id):
    if request.user.role == "Role.A":
        
        if request.method == "POST":
            redemption_request = Redemption_Request.objects.get(pk = request_id)
            
            Redemption_Request.objects.filter(pk = request_id).update(status='Status.A',
                                                                                  approved_by = request.user , 
                                                                                  approved_date = datetime.now())
            
            return render(request,"rewards/admin_redemption_request_view.html",{
                    "redemption_request":redemption_request,
                    "message": "Accpeted"
                    }) 

            
                    
         
def admin_accept_decline_reward (request):
     if (request.user.is_authenticated and request.user.role == "Role.A"):
        suggestion_requests= Suggest_Reward.objects.all()
        return render(request,'rewards/edit_reward.html',{
            'suggestion_requests': suggestion_requests,
        })
         
def delete_reward_suggestion (request, reward_id):
    if (request.user.is_authenticated):
        if request.user.role == "Role.A":
            reward = Suggest_Reward.objects.get(pk = reward_id)
            Suggest_Reward.objects.filter(pk = reward_id).delete()
            
            return render(request,'rewards/edit_reward.html',{
                "Message": f"suggest {reward} has been declined",
            })         

def edit_approve_reward_suggestion(request, reward_id):
    if (request.user.is_authenticated and request.user.role == "Role.A"):
        if(request.method == "POST"):
            try:
                Vendors.objects.create(
                name=request.POST["vendor_name"],
            #  start_date= request.POST["start_date"],
                end_date= request.POST["end_date"],
                img= request.FILES["Image"])
                Suggest_Reward.objects.get(pk = reward_id).delete()
                return redirect('edit_reward')
            except:
                return render(request,'rewards/approve_reward.html',{
                "Message":"Vendor already exists"})
        else:
            reward_suggestion= Suggest_Reward.objects.filter(pk = reward_id)[0]
            return render(request,'rewards/approve_reward.html',{
                'reward_suggestion':reward_suggestion
            })
            
def delete_vendor(request,vendor_id):
    if request.user.role == "Role.A":
        vendor = Vendors.objects.get(pk = vendor_id)
        Vendors.objects.filter(pk = vendor_id).delete()
        vendors = Vendors.objects.filter().all()
        
        return render(request , "rewards/vendors.html",{
            "message":f"Vendor {vendor.name} is Deleted",
             "vendors": vendors
        })
    else:
        return redirect("login")

def put_budget(request):
    if request.user.role == "Role.A":
        now = datetime.now()
    
        if budget.objects.filter(year = int(now.year),is_active = True):
            #creating a piechart
            
            labels = ["Remaining Budget" , "Used Budget"]
            this_year_budget = budget.objects.filter(year = int(now.year),is_active = True)[0].budget
            budget_compare = budget.objects.filter(year = int(now.year),is_active = True)[0].budget_compare
            percentage = (this_year_budget/budget_compare)*100
            data = [percentage,100-percentage]
            print(4)
 
            if request.method == "POST":
                current_budget = budget.objects.filter(year = int(now.year),is_active = True)[0]
                # graph = return_graph(current_budget.budget , current_budget.budget_compare)
                budget_used_percentage = (current_budget.budget/current_budget.budget_compare)*100
                Budget = request.POST["budget"]
                
                points = budget.objects.filter(year = int(now.year))[0].point
                money = budget.objects.filter(year = int(now.year))[0].EGP
                budget.objects.filter(year = int(now.year)).update(is_active = False)
                budget.objects.create(budget = Budget , point = points , EGP = money , budget_compare = Budget)
               
                return redirect("make_budget")
            else:
                current_budget = budget.objects.filter(year = int(now.year),is_active = True)[0]
                budget_used_percentage = (current_budget.budget/current_budget.budget_compare)*100
                return render(request,"rewards/budget.html",{
                "newyear": (now.month == 1 and now.day == 1) or not budget.objects.filter(year = int(now.year),
                                                                                          is_active = True),
                "current_budget":current_budget,
                "budget_used_percentage":budget_used_percentage,
                'labels': labels,
                'data': data,
                
            })
                
        else:
            current_budget = 0
            budget_used_percentage = 0
            labels = ["Remaining Budget" , "Used Budget" ]
            this_year_budget = 0
            budget_compare = 0
            percentage = 0
            data = [percentage,100-percentage]
            
            if request.method == "POST":
             
            
                Budget = request.POST["budget"]
                points = request.POST["points"]
                money = request.POST["EGP"]
                budget.objects.create(budget = Budget , point = points , EGP = money , budget_compare = Budget, admin = request.user)
                
                return redirect("make_budget")
            else:
                return render(request,"rewards/budget.html",{
                    "newyear": (now.month == 1 and now.day == 1) or not budget.objects.filter(year = int(now.year),
                                                                                            is_active = True),
                    "current_budget":current_budget,
                    "budget_used_percentage":budget_used_percentage,
                    'labels': labels,
                    'data': data,
                    
                })
                
                
