from django.test import TestCase, Client
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.
class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com',emp_id = 80)
        self.user.save()
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
    
    def test_load_signup_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
    
    def test_success_register(self):
        response = self.client.post('/', {'username': 'john', 'first_name':'john', 'last_name':'smith', 'password': '123456Mah',
         'confirmation':'123456Mah', 'phone_naumber':'01006459651', 'role':'E', 'emp_id':'9999', 'img':SimpleUploadedFile(name='Picture1.png', 
         content=open('C:/Users/Mahmoud/Desktop/ECS_Reward_System/ECS_Reward_System/media/images/Picture1.png', 'rb').read(), content_type='image/png')})
        test_user = User.objects.find(emp_id=9999)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
        self.assertEqual(test_user.username,'john')