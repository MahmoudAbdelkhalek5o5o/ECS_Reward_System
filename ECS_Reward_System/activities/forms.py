from tkinter.ttk import Style
from .models import Activity, ActivityCategory, ActivityRequest
from django import forms
#from bootstrap_datepicker_plus import DatePickerInput


class SubmitActivityRequestForm(forms.Form):
    activity_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}))
    activity_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}))
    submitted_by = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}))
    evidence_needed = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}), max_length=1024)
    points = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}))
    activity_description_comments = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px; height:100px', 'placeholder': 'Activity details/Comments'}), max_length=1024, required= False)
    date_of_performing_activity = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control', 'style': 'width:350px'}), required= True)
    proof_of_action = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'width:350px'}), required= True)

class CreateNewActivityForm (forms.Form):
    activity_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'style': 'width:350px','required':'True'}),max_length = 30,required=False)
    # categories = ActivityCategory.objects.all()
    # activity_category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category', 'style': 'width:350px'}), choices=[(category.category_name,category.category_name) for category in categories])
    activity_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px; height:100px', 'placeholder': 'Activity details/Comments','required':'True'}), max_length=1024, required= False) 
    evidence_needed = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'style': 'width:350px','required':'True'}), max_length=1024,required=False)
    points = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px','required':'True'}),required=False)
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control', 'style': 'width:350px','required':'True'}), required= False)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control', 'style': 'width:350px'}), required= False)
class UpdateActivityForm(forms.Form):
    activity_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'style': 'width:350px'}),required= False, label='Activity Name')
    activity_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}),required= False )
    points = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}),required= False)
    # attachment_mandatory=forms.BooleanField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled':'true', 'style': 'width:350px'}),required= False)
    evidence_needed= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}), max_length=1024,required= False)
    
    # def clean_activityname(self):
    #     activity_name = self.cleaned_data['activity_name']
    #     if Activity.objects.filter(activity_name=self.activity_name).exists():
    #         raise forms.ValidationError(u'activity "%s" is already in use.' % activity_name)


class UpdateCategoryForm(forms.Form):
    category_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'style': 'width:350px'}),required= False, label='Category Name')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}),required= False, label='Category Description')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'style': 'width:350px'}),required= False, label='End Date')
    budget = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}),required= False, label='Budget')


class SubmitActivitySuggestionForm(forms.Form):
    categories = ActivityCategory.objects.all()
    activity_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}))
    activity_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}))
    justification = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}))
    evidence_needed = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:350px'}))
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category', 'style': 'width:350px'}), choices=[(category.id,category.category_name) for category in categories])
