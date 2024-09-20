from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.submit_application, name='submit_application'),
    path('success/', views.application_success, name='application_success'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reviewer-dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('assign-reviewer/<int:application_id>/', views.assign_reviewer, name='assign_reviewer'),
    path('review-application/<int:application_id>/', views.review_application, name='review_application'),
]