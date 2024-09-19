from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.submit_application, name='submit_application'),
    path('admin/applications/', views.admin_application_list, name='admin_application_list'),
    path('admin/assign-reviewer/<int:application_id>/', views.assign_reviewer, name='assign_reviewer'),
]