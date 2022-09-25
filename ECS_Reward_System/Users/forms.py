from distutils.command import upload
from .models import User
from django import forms
from .models import Role
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



# accounts forms
class SignupForm(forms.Form):
    error_css_class = 'error'
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username',}),min_length=3, max_length = 20, required=False, label='Username')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),min_length=3, max_length = 20, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),min_length=3, max_length = 20, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), required=False)
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), required=False, label = 'Confirm Password')
    number = PhoneNumberField(region="CA",widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), required=False)
    emp_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ID'}), required=False)
    role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Role'}), choices=[(tag, tag.value) for tag in Role])
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs = {'class':'form-control'}), required=False, label='Profile Picture')


    def validate_domain(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        if domain == ecsDomain:
            return True
        return False
    def validate_password(self):
        password = self.cleaned_data['password']
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) 
        and any(x.isdigit() for x in password)):
            return True
        return False

class RegisterForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.pop('role')



class change_password_form(forms.Form):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'style':"width:250px",
        'class': 'form-control mb-4', 'placeholder': 'Enter your password here', 'required': 'True'}),min_length=8, max_length=16)
    New_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'style':"width:250px",
        'class': 'form-control mb-4', 'placeholder': 'Enter your new password here', 'required': 'True'}),min_length=8, max_length=16)
    confirmation = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'style':"width:250px",
        'class': 'form-control', 'placeholder': 'Re-enter your new password', 'required': 'True'}))
    def validate_password(self):
        password = self.cleaned_data['New_password']
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) 
        and any(x.isdigit() for x in password)):
            return True
        return False


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20,min_length=11,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    img = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    def validate_phone_number(self):
        data = self.cleaned_data['phone_number']
        number = data[0:3]
        lines = ['010','011','012','015']
        if not data[1:].isnumeric() or not number in lines:
            return False
        return True
    class Meta:
        model = User
        fields = ['username', 'email','img','phone_number','first_name','last_name']

Roles= [
    ('Role.A', 'Admin'),
    ('Role.M', 'Manager'),
    ('Role.E', 'Employee'),

    ]
class CreateUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username',}),min_length=3, max_length = 20, required=False, label='Username')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),min_length=3, max_length = 20, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),min_length=3, max_length = 20, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), required=False)
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), required=False, label = 'Confirm Password')
    phone_number = PhoneNumberField(region="CA",widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), required=False)
    emp_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ID'}), required=False)
    role = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Role'}), choices=[(tag, tag.value) for tag in Role])
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs = {'class':'form-control'}), required=False, label='Profile Picture')
    role= forms.CharField(label='What is the Users Role?', widget=forms.Select(choices=Roles))


    def validate_domain(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        ecsDomain = "ecs-co.com"
        if domain == ecsDomain:
            return True
        return False
    def validate_password(self):
        password = self.cleaned_data['password']
        if (any(x.isupper() for x in password) and any(x.islower() for x in password) 
        and any(x.isdigit() for x in password)):
            return True
        return False


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    
class UpdateUserrequestForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20,min_length=11,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    role= forms.CharField(label='What is the Users Role?', widget=forms.Select(choices=Roles))
   

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    def validate_phone_number(self):
        data = self.cleaned_data['phone_number']
        number = data[0:3]
        lines = ['010','011','012','015']
        if not data[1:].isnumeric() or not number in lines:
            return False
        return True
    class Meta:
        model = User
        fields = ['username', 'email','phone_number','first_name','last_name', 'role']
        
        

   

