from unicodedata import name
from django.urls import path

from . import views
urlpatterns = [
    path("Create_Vendor",views.create_vendor,name = "create_vendor"),
    path("vendors",views.view_vendors, name = "all_vendors"),
    path("vendors/<int:vendor_id>", views.vendor_view , name="vendor"),
    path("Create_Reward",views.add_new_reward,name = "create_reward"),
    path("suggest_rewards",views.suggest_rewards,name = "suggest_rewards"),
    path("<int:voucher_id>",views.redemption_request, name = "redemption_request"),
    path("Admin_view_redemption_requests",views.admin_view_redemption_requests,name = "admin_view_redemption_requests"),
    path("admin_view_redemption_requests/<int:redemption_request_id>", views.redemption_request_view, name = "view_redemption_request"),
    path('redemption_request/<int:request_id>/', views.decline_redemption, name='redemption_decline'),
    path('redemption_request_accept/<int:request_id>/', views.accept_redemption, name='accept'),
    path("edit_reward", views.admin_accept_decline_reward, name="edit_reward"),
    path("delete_reward_suggestion/<int:reward_id>", views.delete_reward_suggestion, name="delete_reward_suggestion"),
    path("edit_approve_reward_suggestion/<int:reward_id>", views.edit_approve_reward_suggestion, name="edit_approve_reward_suggestion"),
    path("<int:vendor_id>/deletevendor",views.delete_vendor,name = "delete_vendor"),
    path("put_budget",views.put_budget, name="make_budget")
]
