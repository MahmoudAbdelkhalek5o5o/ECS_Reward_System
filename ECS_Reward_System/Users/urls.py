from django.urls import path

from . import views



urlpatterns = [
    path("sign_up",views.register, name="register"),
    path("",views.login_view,name = "login"),
    path("logout",views.logout_view, name = "logout"),
    path("homescreen/change_password", views.change_password, name='change_password'),
    path('accounts/edit_user/', views.userEdit, name='user_edit'),
    path('accounts/Admin_register_request/', views.Admin_View_register_request, name='register_request'),
    path('<int:request_id>/accepted/', views.Admin_accept_register, name='register_accept'),
    path('<int:request_id>/rejected/', views.Admin_reject_register, name='register_reject'),
    path('request/<int:emp_id>', views.view_profile, name='view_profile'),
    path('edit_request/<int:emp_id>', views.edit_register_request, name='edit_request'),
    path('profile_view',views.profiles , name = "all_profiles"),
    path('profile_view/Create_Account',views.admin_create_user , name = "admin_create_user"),
    
]
