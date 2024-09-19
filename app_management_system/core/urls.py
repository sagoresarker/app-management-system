from django.urls import path
from .views import register, login_view, logout_view, activate, registration_complete

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('registration_complete/', registration_complete, name='registration_complete'),
]
