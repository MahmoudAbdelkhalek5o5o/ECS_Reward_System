from asyncio.windows_events import NULL
from contextlib import nullcontext
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect
from datetime import datetime,date,timedelta
from django.core.mail import send_mail

from .models import ActivityCategoryEdit, ActivityEdit, ActivityRequest, Activity, ActivityCategory ,Points,ActivitySuggestion
from Users.models import User ,announcements
from Rewards.models import budget
import pytz
from .forms import SubmitActivityRequestForm,CreateNewActivityForm,UpdateCategoryForm,UpdateActivityForm,SubmitActivitySuggestionForm
from django.forms.models import model_to_dict


# Create your views here.




def submit_activity_request(request):
    if(request.user.is_authenticated):
        if request.user.role == "Role.M":
            return render_submit_activity_request_by_manager_page(request)
        if request.user.role == "Role.E":
            return render_submit_activity_request_by_employee_page(request)
        if request.user.role == "Role.A":
            return render(request,'activity/submit_activity_request_form.html',{
            'form': "You can not submit Activity Requests"
        })


def render_submit_activity_request_by_employee_page(request):
    if request.method == "POST":
        if("choose" in request.POST):
            return render_submit_activity_request_page(request)
        else:
            return submit_activity_request_by_employee(request)
    else:
        return category_view(request)
def render_submit_activity_request_by_manager_page(request):
    if request.method == "POST":
        if("choose" in request.POST):
            return render_submit_activity_request_page(request)
        else:
            return submit_activity_request_by_manager(request)
    else:
        return category_view(request)


def render_submit_activity_request_page(request):
    # retrieve selected activity_data to be ssdisplayed in the form
    activity_id = request.POST["choose"]
    activity_data = list(Activity.objects.filter(pk=activity_id).values())[0]
    activity_category = list(ActivityCategory.objects.filter(pk=activity_data["category_id"]).values())[0]["category_name"]
    activity_data["activity_category"] = activity_category
    activity_data["submitted_by"] = request.user.username
    # add the data to the form
    form = SubmitActivityRequestForm(initial = activity_data)
    # render the page
    return render(request,'activity/submit_activity_request_form.html',{
        'form': form,
        'activity':activity_data,
        'activity_id':activity_id
    })
def submit_activity_request_by_employee(request):
    # collect the activity_request_data
    print(request.POST['activity_id'])
    activity_data = list(Activity.objects.filter(pk=request.POST["activity_id"]).values())[0]
    activity = Activity.objects.filter(pk=request.POST["activity_id"])[0]
    category = ActivityCategory.objects.filter(pk=activity_data["category_id"])[0]
    activity_data["submitted_by"] = request.user.username
    activity_data["activity_category"] = category.category_name
    activity_data['activity_description_comments'] = request.POST['activity_description_comments']
    activity_data['date_of_performing_activity'] = request.POST['date_of_performing_activity']
    activity_data['activity_id'] = request.POST['activity_id']
    form = SubmitActivityRequestForm(activity_data)
    # format the string date to datetime
    date = datetime.strptime(request.POST["date_of_performing_activity"].replace('-','/'), '%Y/%m/%d')
    # check if the user submits for himself or for someone
    if request.POST['submitted_to'] == '':
        user = request.user
    else:
        try:
            user = User.objects.filter(pk = request.POST['submitted_to'])[0]
            if user.role == 'Role.A':
                return render(request,'activity/submit_activity_request_form.html',{
                'form': form,
                'failure_message':'user does not exist in the table',
                'activity_id':request.POST['activity_id']
            })
        except:
            return render(request,'activity/submit_activity_request_form.html',{
                'form': form,
                'failure_message':'user does not exist in the table',
                'activity_id':request.POST['activity_id']
            })
    # can't submit request of activity that belongs to the category owner
    if user.emp_id == category.owner_id:
        return render(request,'activity/submit_activity_request_form.html',{
        'form': form,
        'failure_message':'You can not submit activity that belongs to the submitter category',
        'activity_id':request.POST['activity_id']

    })
  
    # add the activity_request to the database
    ActivityRequest.objects.create(emp = user, submission_date=date, end_date=date + timedelta(days=30), category=category,
    status = "Status.P", approved_by = User(), activity = activity,  proof_of_action = request.FILES["proof_of_action"],
    activity_approval_date = date, evidence_needed=activity.evidence_needed)
   
    return redirect('activities:activity_request_view')
def submit_activity_request_by_manager(request):
     
    activity_data = list(Activity.objects.filter(pk=request.POST["activity_id"]).values())[0]
    activity = Activity.objects.filter(pk=request.POST["activity_id"])[0]
    category = ActivityCategory.objects.filter(pk=activity_data["category_id"])[0]
    activity_data["submitted_by"] = request.user.username
    activity_data["activity_category"] = category.category_name
    activity_data['activity_description_comments'] = request.POST['activity_description_comments']
    activity_data['date_of_performing_activity'] = request.POST['date_of_performing_activity']
    activity_data['activity_id'] = request.POST['activity_id']
    form = SubmitActivityRequestForm(activity_data)
    # format the string date to datetime
    date = datetime.strptime(request.POST["date_of_performing_activity"].replace('-','/'), '%Y/%m/%d')
    # check if the user submits for himself or for someone
    if request.POST['submitted_to'] == '':
        user = request.user
    else:
        try:
            user = User.objects.filter(pk = request.POST['submitted_to'])[0]
            if user.role == 'Role.A':
                return render(request,'activity/submit_activity_request_form.html',{
                'form': form,
                'failure_message':'user does not exist in the table',
                'activity_id':request.POST['activity_id']
            })
        except:
            return render(request,'activity/submit_activity_request_form.html',{
                'form': form,
                'failure_message':'user does not exist in the table',
                'activity_id':request.POST['activity_id']
            })
    # can't submit request of activity that belongs to the category owner
    if user.emp_id == category.owner_id:
        return render(request,'activity/submit_activity_request_form.html',{
        'form': form,
        'failure_message':'You can not submit activity that belongs to the submitter category',
        'activity_id':request.POST['activity_id']

    })
    # add the activity_request to the database
    ActivityRequest.objects.create(emp = user, submission_date=date, end_date = date + timedelta(days=30), category=category,
     status = "Status.P", activity = activity,  proof_of_action = request.FILES["proof_of_action"],
     activity_approval_date = date, evidence_needed=activity.evidence_needed)
    return redirect('activities:activity_request_view')



def category_view(request):
    if (request.method=="GET"):
        category= ActivityCategory.objects.filter(is_archived = False)
        category_list = []
        utc=pytz.UTC
        now = utc.localize(datetime.now())
        for cat in category:
            if cat.start_date <= now:
                category_list.append(cat)
        approved = Activity.objects.filter(is_approved = True)
        activities_categorized = []
        activities = Activity.objects.filter(is_approved = True).all()
        
        used_up_budget = ActivityCategory.objects.filter(budget = 0)
      
            
        for category in category_list:
            if category.end_date:
                if now > category.end_date:
                    ActivityCategory.objects.filter(pk = category.id).update(is_archived = True)  
        for activity in activities:
            if activity.end_date:
                if now > activity.end_date:
                    Activity.objects.filter(pk = activity.id).update(is_archived = True)  
        for category in category_list:
            categ_id = category.id
            activities=list(Activity.objects.filter(category = categ_id).values())
            now = utc.localize(datetime.now())
            activities_categorized.append({'id':category.id,'category_name':category.category_name,'category_activities':activities,"budget":category.budget})
        if request.user.role == "Role.M":
            return render(request,"activity/categ_view_manager.html",{
                "category_list":category_list,
                "activities_categorized":activities_categorized,
                "approved":approved,
                "activities":activities,
                'message': "Activity has been successfully submitted",
                "used_up_budget":used_up_budget,})
        else:
             return render(request,"activity/categ_view.html",{
                "category_list":category_list,
                "activities_categorized":activities_categorized,
                "approved":approved,
                "activities":activities,
                'message': "Activity has been successfully submitted",
                "used_up_budget":used_up_budget,})
    
def delete_category(request, category_id):
    if request.user.is_authenticated:
        if request.user.role == 'Role.A':
            ActivityCategory.objects.filter(pk=category_id).update(is_archived = True)
            return redirect('activities:Category_view')
        else:
            return redirect("users-home")
    else:
        return redirect('login')
def manager_view_activity_submission_request(request):
    if request.user.is_authenticated and request.user.role == "Role.M":
        activity_submissions = ActivityRequest.objects.filter(status='Status.P').all()
        
        return render(request,"activity/manager_view_submission.html",{
            "activity_submissions":activity_submissions,
})
    else:
        return redirect("login")

def activity_submission_view(request,activity_submission_id):
    activity_submission = ActivityRequest.objects.get(pk = activity_submission_id)
    return render(request,"activity/submission_view.html",{"activity_submission":activity_submission}) 

def manager_accept_activity(request,request_id):
    if request.user.role == "Role.M":
        #Grab the submission by its id
        activity_submissions = ActivityRequest.objects.get(pk = request_id)
        #get the budget
        Budget = budget.objects.filter(year = int(datetime.now().year) , is_active = True)[0]
        if request.method == "POST":
            conversion = activity_submissions.activity.points//Budget.point
            #update the points
            budget.objects.filter(year = int(datetime.now().year) , is_active = True).update(budget = Budget.budget - conversion)
            ActivityCategory.objects.filter(pk = activity_submissions.activity.category.id).update(budget = activity_submissions.activity.category.budget - conversion)
            Points.objects.create(points = activity_submissions.activity.points ,
                             amounts = conversion , end_date =  datetime.now() + timedelta(days=183) ,
                             employee = activity_submissions.emp)
            ActivityRequest.objects.filter(pk = request_id).update(status='Status.A')
            User.objects.filter(pk = activity_submissions.emp.emp_id).update(points = activity_submissions.activity.points + activity_submissions.emp.points)
            #activity_submission.save()
            send_mail(
                    'Activity Request',
                    'Your activity request has been accepted, the equivalent points have been added to your aaccount',
                    'muhammad.mazen4@gmail.com',
                    [f'{activity_submissions.emp.email}'],
                    fail_silently=False,
                                        )
            return redirect("activities:activity_submission_view")
        else:
            return redirect("users-home")
    else:
        return redirect("login")

def manager_decline_activity(request,request_id):
    if request.user.role == "Role.M":
        ActivityRequest.objects.get(pk = request_id)
        if request.method == "POST":
            
            ActivityRequest.objects.filter(pk = request_id).update(status='Status.D')
            #activity_submission.save()
            send_mail(
                    'Activity Request',
                    'Your activity request has been rejected',
                    'muhammad.mazen4@gmail.com.com',
                    ['youssef.ismail@ecs-co.com'],
                    fail_silently=False,
                                        )
            return redirect("activities:activity_submission_view")
        else:
            return redirect("users-home")
    else:
        return(redirect("login"))
def admin_view_activity_submission_request(request):
    if request.user.is_authenticated and request.user.role == "Role.A":
        activity_submissions = ActivityRequest.objects.filter(status='Status.A') | ActivityRequest.objects.filter(status='Status.D')
        
        return render(request,"activity/admin_view_submission.html",{
            "activity_submissions":activity_submissions,
})
def activity_submission_admin(request,activity_submission_id):
    activity_submission = ActivityRequest.objects.get(pk = activity_submission_id)
    return render(request,"activity/activity_submission_admin.html",{"activity_submission":activity_submission})

def admin_return_activity(request,request_id):
    if request.user.role == "Role.A":
        activity_submissions = ActivityRequest.objects.get(pk = request_id)
        if request.method == "POST":
            
            ActivityRequest.objects.filter(pk = request_id).update(status='Status.P')
            User.objects.filter(pk = activity_submissions.emp.emp_id).update(points = activity_submissions.emp.points - activity_submissions.activity.points)
            # activity_submission=ActivityRequest.emp_id.p
            #activity_submission.save()
            send_mail(
                    'Activity Request review',
                    'Your activity request has been return to category owner, the equivalent points have been deducted from your aaccount',
                    'muhammad.mazen4@gmail.com.com',
                    [f'{activity_submissions.emp.email}'],
                    fail_silently=False,
                                        )
            return redirect("activities:admin_view_submission")
        else:
            return redirect("users-home")
    else:
        return redirect("login")



def admin_return_points(request,request_id):
    
    if request.user.role == "Role.A":
        
        activity_submissions = ActivityRequest.objects.get(pk = request_id)
        if request.method == "POST":
            
            
            ActivityRequest.objects.filter(pk = request_id).update(status='Status.D')
            User.objects.filter(pk = activity_submissions.emp.emp_id).update(points = activity_submissions.emp.points - activity_submissions.activity.points)
            #activity_submission.save()
            send_mail(
                    'Activity Request',
                    'We are sorry to inform you that we had to deduct points from your account',
                    'muhammad.mazen4@gmail.com.com',
                    ['youssef.ismail@ecs-co.com'],
                    fail_silently=False,)
            return redirect("activities:admin_view_submission")
        else:
            return redirect("users-home")
    

def activity_request_view(request):
    #grab the activity by the employee id
    activity_requests=ActivityRequest.objects.filter(emp_id=request.user.emp_id).select_related("category","activity")

    return render(request,"activity/activity_requests_view.html",{
        "activity":activity_requests
    })


def points_view(request):
    #grab the points from the User Model by the employee id
    points = User.objects.get(pk = request.user.emp_id).points
    print(points)
    
    #send the Points to the Points view page
    return render(request,"activity/points_view.html",{
        "points":points
})
def delete_activity(request,activity_id):
    activity = Activity.objects.get(pk = activity_id)
    if request.user.role == "Role.A":
        Activity.objects.filter(pk = activity_id).update(is_archived = True)
        return redirect("activities:Category_view")
    
def sure_delete(request,activity_id):
        if request.user.role == "Role.A":
            activity = Activity.objects.filter(pk = activity_id)
            if request.method == "POST":
                activity.delete()
                return redirect("activities:Category_view")
def not_sure_delete(request,activity_id):
    if request.method == "POST":
        return redirect("activities:Category_view")
    
    
def points_about_expire(request):
    if not request.user.role == "Role.A":
        result = []
        points_categorized = []
        utc=pytz.UTC
        now = utc.localize(datetime.now())  
        points = Points.objects.filter(employee = request.user)
        expired_points = Points.objects.filter(employee=request.user,is_used = False)
        used_points=Points.objects.filter(employee=request.user, is_used=True)
      
        for point in expired_points:
            if now > point.end_date:
                 points_categorized.append(point)
        for point in points:
            delta = point.end_date - now
            if delta.days <= 30 and point.is_used == False and delta.days > 0:
                result.append(point)
        return render(request,"activity/Points_view.html",{
            "points":result,
            "used_points":used_points,
            "expired_points": points_categorized,
        })
    else:
        return redirect("login")
def create_new_activity(request):
    if not request.user.role == "Role.E" :
        if request.user.role == "Role.M":
            activity_category = ActivityCategory.objects.filter(owner = request.user).all()
        else:
            activity_category = ActivityCategory.objects.all()
        if request.method== 'POST':
            form= CreateNewActivityForm(request.POST)
            if form.is_valid():
                activity_name= request.POST["activity_name"]
                category = ActivityCategory.objects.get(pk = request.POST["category_select"])
                activity_description= request.POST["activity_description"]
                evidence_needed= request.POST["evidence_needed"]
                Points= request.POST["points"]  
                start_date = request.POST["start_date"]
                end_date = request.POST["end_date"]
                category_budget = ActivityCategory.objects.get(pk = category.id).budget
                points_check = int(Points)/budget.objects.filter(year = int(datetime.now().year),is_active = True)[0].point
            
                if request.user.role == "Role.M":
                    
                    if points_check <= category_budget:
                        if end_date:
    
                            Activity.objects.create(activity_name= activity_name, category = category , 
                                                    activity_description=activity_description,
                            evidence_needed=evidence_needed, points=Points, attachment_mandatory= True, 
                            start_date = start_date, end_date = end_date)
                        else:
                            Activity.objects.create(activity_name= activity_name, category = category , 
                                                    activity_description=activity_description,
                            evidence_needed=evidence_needed, points=Points, attachment_mandatory= True, 
                            start_date = start_date)
                      
                        return render(request,"activity/create_new_activity.html" ,{
                            "form": form,
                            'message': "Activity has been successfully submitted for review.",
                            "activity_category":activity_category
                            })
                    else:
                        return render (request, "activity/create_new_activity.html" ,{
                            "form": form,
                            'error_message': f"You can't set points with monetary value greater than the category budget",
                            "activity_category":activity_category
                            }) 
                else:
                    if points_check <= category_budget:
                        if end_date:
    
                            Activity.objects.create(activity_name= activity_name, category = category , 
                                                    activity_description=activity_description,
                            evidence_needed=evidence_needed, points=Points, attachment_mandatory= True, 
                            start_date = start_date, end_date = end_date)
                        
                            Activity.objects.create(activity_name= activity_name, category = category , activity_description=activity_description,
                            evidence_needed=evidence_needed, points=Points, attachment_mandatory= True, start_date = start_date, end_date = end_date,is_approved = True)
                        else:
                            Activity.objects.create(activity_name= activity_name, category = category , 
                                                    activity_description=activity_description,
                            evidence_needed=evidence_needed, points=Points, attachment_mandatory= True, 
                            start_date = start_date )
                        
                            
                            
                         
                        form= CreateNewActivityForm()
                        return render (request, "activity/create_new_activity.html" ,{
                            "form": form,
                            'message': "Activity has been successfully submitted",
                            "activity_category":activity_category
                            }) 
                    else:
                        return render (request, "activity/create_new_activity.html" ,{
                            "form": form,
                            'error_message': f"You can't set points with monetary value greater than the category budget",
                            "activity_category":activity_category
                            }) 
            else:           
                form= CreateNewActivityForm()
                return render (request, "activity/create_new_activity.html" , {"form": form,
                'failure_message': "invalid input",
                "activity_category":activity_category
                }) 
        else:
            # list=ActivityCategory.objects.filter(owner=request.user.emp_id).values("category_name")
            form= CreateNewActivityForm({"activity_category":list})
            return render (request, "activity/create_new_activity.html" , {
                "form": form,
                "activity_category":activity_category
                
})
def submit_suggestion(request):
    if request.method== "POST":
        if request.user.role == "Role.M" or "Role.E":
            getactivityname= request.POST['name']
            getactivitycategory= ActivityCategory.objects.filter(category_name=request.POST['activity_category'])[0]
            
            getactivitydescription= request.POST['description']
            getjustification= request.POST['justification']
            getevidence= request.POST['evidence']
            ActivitySuggestion.objects.create(activity_name = getactivityname , category=getactivitycategory, activity_description=getactivitydescription, justification=getjustification,
            evidence_needed = getevidence,)
            categories= ActivityCategory.objects.all()
            return render(request,"activity/submit_suggestion.html", {
                'categories': categories,
                'message': "Activity has been successfully submitted"
            })
    
    else:
        categories= ActivityCategory.objects.all()
        print(categories)
        return render(request,"activity/submit_suggestion.html", {
            'categories': categories,
            
        })


    
        
def edit_activity(request,activity_id):
    if request.user.is_authenticated and request.user.role == "Role.A":
        if request.method == 'POST':
            activity_edit_form = UpdateActivityForm(request.POST)
            if activity_edit_form.is_valid():
                print(Activity.objects.filter(activity_name=request.POST["activity_name"]).exists())
                print(request.POST["activity_name"])
                if Activity.objects.filter(activity_name=request.POST["activity_name"]).exists():
                    return redirect("activities:Category_view")
                else:
                    activity_name=request.POST["activity_name"]
                    activity_description=request.POST["activity_description"]
                    points=request.POST["points"]
                    evidence_needed=request.POST["evidence_needed"]
                    Activity.objects.filter(pk = activity_id).update(activity_name=activity_name,
                    activity_description=activity_description,points=points,evidence_needed=evidence_needed)
                    return redirect("activities:Category_view")
        else:
            this_activity=Activity.objects.filter(pk = activity_id)[0]
            activity_edit_form=UpdateActivityForm({"activity_name":this_activity.activity_name,
            "activity_description":this_activity.activity_description,"points":this_activity.points,"evidence_needed":this_activity.evidence_needed})
            return render(request,"activity/edit_and_approve_activity.html",{"form":activity_edit_form})
def edit_category(request,ActivityCategory_id):
    if request.user.is_authenticated and request.user.role == "Role.A":
        if request.method == 'POST':
            category_edit_form = UpdateCategoryForm(request.POST)
            if category_edit_form.is_valid():
                if ActivityCategory.objects.filter(category_name=request.POST["category_name"]).exists() and ActivityCategory.objects.get(pk=ActivityCategory_id).description == request.POST["description"]:
                    return render(request,"activity/edit_category.html",{
                        "category_edit_form":category_edit_form,
                        "Message":"Category Name already exists or you haven't changed the form"
                        })
                else:
                    category_name=request.POST["category_name"]
                    description=request.POST["description"]
                    end_date = request.POST["end_date"]
                    Budget  =  request.POST["budget"]
                    if end_date:
                        ActivityCategory.objects.filter(pk = ActivityCategory_id).update(category_name=category_name,
                        description=description , end_date = end_date , budget = Budget)
                    else:
                        ActivityCategory.objects.filter(pk = ActivityCategory_id).update(category_name=category_name,
                        description=description , budget = Budget)
                        
                    return render(request,"activity/edit_category.html",{
                        "category_edit_form":category_edit_form,
                        "success":"Category Updated"
                        })
        else:
            this_category=ActivityCategory.objects.filter(pk = ActivityCategory_id)[0]
            category_edit_form=UpdateCategoryForm({"category_name":this_category.category_name,
            "description":this_category.description ,"budget":this_category.budget , "end_date":this_category.end_date})
            return render(request,"activity/edit_category.html",{"category_edit_form":category_edit_form})  
                
                
def view_activity_suggestion_requests(request):
    if(request.user.is_authenticated):
        if(request.user.role == "Role.A"):
            suggestion_requests = ActivitySuggestion.objects.all()
            return render(request,'activity/view_activity_suggestion_requests.html',{
                'suggestion_requests': suggestion_requests
            })
        if (request.user.role == "Role.M"):
            suggestion_requests = ActivitySuggestion.objects.none()
            categories = ActivityCategory.objects.filter(owner_id = request.user)
            for category in categories:
                suggestion_requests |= ActivitySuggestion.objects.filter(category = category)
            return render(request,'activity/view_activity_suggestion_requests.html',{
                'suggestion_requests': suggestion_requests
            })
        else:
            return redirect('users-home')
    else:
        return redirect('login')

def delete_activity_suggestion_request(request, suggestion_id):
    if (request.user.is_authenticated):
        if request.user.role == "Role.A" or request.user.role == "Role.M":
            ActivitySuggestion.objects.get(pk = suggestion_id).delete()
            return redirect('activities:view_activity_suggestion_requests')

def delete_not_approved_activity(request, activity_id):
    if (request.user.is_authenticated):
        if request.user.role == "Role.A":
            Activity.objects.get(pk = activity_id).delete()
            return redirect('activities:view_not_approved_activities')

    
def edit_activity_suggestion_and_submit(request, suggestion_id):
    if (request.user.is_authenticated):
        if request.user.role == "Role.M" or request.user.role == "Role.A":
            if(request.method == "POST"):
                Activity.objects.create(activity_name=request.POST["activity_name"],
                activity_description=request.POST["activity_description"], points = request.POST["points"], attachment_mandatory = request.POST["attachment_mandatory"],
                evidence_needed = request.POST['evidence_needed'], start_date = request.POST['start_date'],end_date = request.POST['end_date'],
                category = ActivityCategory.objects.filter(pk = request.POST['category'])[0], is_approved = False)
                ActivitySuggestion.objects.filter(pk = suggestion_id).delete()
                return redirect('activities:view_activity_suggestion_requests')
            else:
                suggestion = model_to_dict(ActivitySuggestion.objects.filter(pk = suggestion_id)[0])
                form = SubmitActivitySuggestionForm(suggestion)
                return render(request,'activity/edit_suggestion.html',{
                    'form':form
                })
        else:
            return redirect('users-home')
    else:
        return redirect('login')



def manager_submits_activity(request, suggestion_id):
    if(request.user.is_authenticated):
        if request.user.role == "Role.M":
            suggestion = ActivitySuggestion.objects.filter(pk = suggestion_id)[0]
            Activity.objects.create(is_approved = False, activity_name = suggestion.activity_name,
            activity_description=suggestion.activity_description, points= request.POST['points'],
            evidence_needed = suggestion.evidence_needed)
        else:
            return redirect('users-home')
    else:
        return redirect('login')

def view_not_approved_activities(request):
    if(request.user.is_authenticated):
        if(request.user.role == "Role.A"):
            activities = Activity.objects.filter(is_approved=False)
            return render(request,'activity/view_not_approved_activities.html',{
                'activities': activities
            })
        else:
            return redirect('users-home')
    else:
        return redirect('login')



def edit_and_approve_activity(request, activity_id):
    if (request.user.is_authenticated):
        activity_select = Activity.objects.get(pk = activity_id)
        if request.user.role == "Role.A":
            if(request.method == "POST"):
                if activity_select.end_date:
                    Activity.objects.filter(pk=activity_id).update(activity_name=request.POST["activity_name"],
                    activity_description=request.POST["activity_description"], points = request.POST["points"],
                    evidence_needed = request.POST['evidence_needed'], start_date = request.POST['start_date'],end_date = request.POST['end_date'], is_approved = True)
                else:
                    Activity.objects.filter(pk=activity_id).update(activity_name=request.POST["activity_name"],
                    activity_description=request.POST["activity_description"], points = request.POST["points"],
                    evidence_needed = request.POST['evidence_needed'], start_date = request.POST['start_date'], is_approved = True)
                
                return redirect('activities:view_not_approved_activities')
                
            else:
                categories = ActivityCategory.objects.all()
                activity_object = Activity.objects.filter(pk = activity_id)[0]
                activity = model_to_dict(activity_object)
                activity['start_date'] = activity_object.start_date.date()
                if activity_select.end_date:
                    activity['end_date'] = activity_object.end_date.date()
                form = CreateNewActivityForm(activity) 
                return render(request,'activity/edit_and_approve_activity.html',{
                        'form':form,
                        'categories': categories
                })
        else:
            return redirect('users-home')
    else:
        return redirect('login')        
    
def create_category(request):
    if request.user.role == "Role.A":
        if budget.objects.filter(year = int(datetime.now().year), is_active = True):
            #grab the System budget by the current year and if its currently active
            system_budget = budget.objects.filter(year = int(datetime.now().year), is_active = True)[0]
        #get all category owners
        category_owners = User.objects.filter(role = "Role.M")
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            end_date = request.POST["end_date"]
            Owner = request.POST["owner"]
            Budget = request.POST["Budget"]
            start_date = request.POST['start_date']
    
            #checks if admin added valid budget for category
            if int(Budget) < system_budget.budget and not ActivityCategory.objects.filter(category_name=request.POST["name"]).exists():
                if end_date:
                    
                    ActivityCategory.objects.create(category_name = name , end_date = end_date , 
                                                    owner = User.objects.get(username = Owner) , 
                                                    description = description,budget = Budget , budget_compare = Budget , start_date = start_date)
                    announcements.objects.create(creator = request.user , PostText = f"A new Activity {name} is added!!",EndDate = datetime.now() + timedelta(days=30))
                    return render(request,"activity/create_category.html",{
                    "message":"Category successfuly added",
                    "category_owners": category_owners
                    })
                else:
                    
                    ActivityCategory.objects.create(category_name = name  , 
                                                    owner = User.objects.get(username = Owner) , 
                                                    description = description,budget = Budget , budget_compare = Budget , start_date = start_date)
                    announcements.objects.create(creator = request.user , PostText = f"A new Activity {name} is added!!",EndDate = datetime.now() + timedelta(days=30))
                    return render(request,"activity/create_category.html",{
                    "message":"Category successfuly added",
                    "category_owners": category_owners
                    })
                    
            elif ActivityCategory.objects.filter(category_name=request.POST["name"]).exists():
                return render(request,"activity/create_category.html",{
                    "warning_message":"category Already Exists try adding activities to that category",
                    "category_owners": category_owners

                })
                
            elif int(Budget) > system_budget.budget:
                    return render(request,"activity/create_category.html",{
                    "error_message": f"Category budget ({Budget}) can't be higher than System Budget ({system_budget.budget})",
                    "category_owners": category_owners
                })
        else:
            return render(request,"activity/create_category.html",{
                "category_owners": category_owners
            })
def category_edit_delete(request):
        if request.user.is_authenticated and request.user.role == "Role.M":
            if(request.method == "POST"):
                pass
            
        
# manager request editing activity
def edit_activity_manager(request,activity_id):
    if request.user.is_authenticated and request.user.role == "Role.M":
        if request.method == 'POST':
            activity_edit_form = UpdateActivityForm(request.POST)
            if activity_edit_form.is_valid():
                if Activity.objects.filter(activity_name=request.POST["activity_name"]).exists():
                    return redirect("activities:Category_view_manager")
                else:
                    activity = Activity.objects.get(pk = activity_id)
                    activity_name=request.POST["activity_name"]
                    activity_description=request.POST["activity_description"]
                    points=request.POST["points"]
                    evidence_needed=request.POST["evidence_needed"]
                    ActivityEdit.objects.create(original_activity=activity,activity_name=activity_name,
                    activity_description=activity_description,points=points,evidence_needed=evidence_needed, edited = True, deleted=False)
                    return redirect("activities:Category_view_manager")
        else:
            this_activity=Activity.objects.filter(pk = activity_id)[0]
            activity_edit_form=UpdateActivityForm({"activity_name":this_activity.activity_name,
            "activity_description":this_activity.activity_description,"points":this_activity.points,"evidence_needed":this_activity.evidence_needed})
            return render(request,"activity/edit_and_approve_activity.html",{"form":activity_edit_form})



# manager requests editing his category

def edit_category_manager(request,ActivityCategory_id):
    if request.user.is_authenticated and request.user.role == "Role.M" and request.user.emp_id == ActivityCategory.objects.get(pk = ActivityCategory_id).owner:
        if request.method == 'POST':
            category_edit_form = UpdateCategoryForm(request.POST)
            if category_edit_form.is_valid():
                if ActivityCategory.objects.filter(category_name=request.POST["category_name"]).exists() and ActivityCategory.objects.get(pk=ActivityCategory_id).description == request.POST["description"]:
                    return render(request,"activity/edit_category.html",{
                        "category_edit_form":category_edit_form,
                        "Message":"Category Name already exists or you haven't changed the form"
                        })
                else:
                    category = ActivityCategory.objects.get(pk = ActivityCategory_id)
                    category_name=request.POST["category_name"]
                    description=request.POST["description"]
                    end_date = request.POST["end_date"]
                    Budget  =  request.POST["budget"]
                    if end_date:
                        ActivityCategoryEdit.objects.create(original_category = category, category_name=category_name,
                        description=description , end_date = end_date , budget = Budget, edited = True, deleted = False)
                    else:
                        ActivityCategoryEdit.objects.create(original_category = category, category_name=category_name,
                        description=description , budget = Budget, edited = True, deleted = False)
                        
                    return render(request,"activity/edit_category.html",{
                        "category_edit_form":category_edit_form,
                        "success":"Category Updated"
                        })
        else:
            this_category=ActivityCategory.objects.filter(pk = ActivityCategory_id)[0]
            category_edit_form=UpdateCategoryForm({"category_name":this_category.category_name,
            "description":this_category.description ,"budget":this_category.budget , "end_date":this_category.end_date})
            return render(request,"activity/edit_category.html",{"category_edit_form":category_edit_form})  