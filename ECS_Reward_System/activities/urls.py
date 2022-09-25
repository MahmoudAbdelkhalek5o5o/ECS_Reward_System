from django.urls import path

from . import views
app_name = 'activities'
urlpatterns = [
    path('submit_activity_request',views.submit_activity_request,name = 'submit_activity_request'),
    path('Category_view',views.category_view, name = 'Category_view'),
    path('Category_view_manager',views.category_view, name = 'Category_view_manager'),
    path('edit_activity_manager/<int:activity_id>', views.edit_activity_manager, name= 'edit_activity_manager'),
    path('edit_category_manager/<int:ActivityCategory_id>', views.edit_category_manager, name= 'edit_category_manager'),
    path('activity_request_view',views.activity_request_view, name ='activity_request_view'),
    path('points_view',views.points_view, name ='points_view'),
    path('manager_view_submission/', views.manager_view_activity_submission_request, name='activity_submission_view'),
    path("manager_view_submission/<int:activity_submission_id>", views.activity_submission_view, name = "submission"),
    path('<int:request_id>', views.manager_accept_activity, name='activity_accept'),
    path('submission_view/<int:request_id>/', views.manager_decline_activity, name='activity_decline'),
    path('activity/admin_view_requests', views.admin_view_activity_submission_request, name='admin_view_submission'),
    path('admin_view_submission/<int:activity_submission_id>', views.activity_submission_admin, name = "submission_admin"),
    path('<int:request_id>/returntocategoryowner', views.admin_return_activity, name='return_request'),
    path('<int:request_id>/returnpoints', views.admin_return_points, name='returnpoints'),
    path('admin_delete_activity/<int:activity_id>', views.delete_activity, name = "delete_activity"),
    path('sure_delete_activity/<int:activity_id>', views.sure_delete, name = "sure_delete_activity"),
    path('not_sure_delete_activity/<int:activity_id>', views.not_sure_delete, name = "not_sure_delete_activity"),
    path('My_Points' , views.points_about_expire , name = "about_to_expire"),
    path('create_new_activity', views.create_new_activity, name= "create_new_activity"),
    path('submit_suggestion/', views.submit_suggestion, name= "submit_suggestion"),
    path('edit_activity/<int:activity_id>', views.edit_activity, name = "edit_activity"),
    path('edit_category/<int:ActivityCategory_id>', views.edit_category, name = "edit_category"),
    path('view_activity_suggestion_requests', views.view_activity_suggestion_requests, name = "view_activity_suggestion_requests"),
    path('delete_suggestion/<int:suggestion_id>',views.delete_activity_suggestion_request, name = 'delete_suggestion'),
    path('edit_suggestion_and_submit/<int:suggestion_id>',views.edit_activity_suggestion_and_submit, name = 'edit_suggestion_and_submit'),
    path('manager_submits_activity', views.manager_submits_activity, name = 'manager_submits_activity'),
    path('view_not_approved_activities', views.view_not_approved_activities, name = 'view_not_approved_activities'),
    path('delete_not_approved_activity/<int:activity_id>', views.delete_not_approved_activity, name = "delete_not_approved_activity"),
    path('edit_and_approve_activity/<int:activity_id>', views.edit_and_approve_activity, name = "edit_and_approve_activity"),
    path('create_categ',views.create_category,name = "create_category"),
    path('delete_category/<int:category_id>', views.delete_category, name='delete_category')

    
]