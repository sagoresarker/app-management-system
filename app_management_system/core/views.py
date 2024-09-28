from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until email confirmation
            user.save()

            # Send activation email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            activation_link = f"http://{domain}/activate/{uid}/{token}/"

            subject = 'Activate Your Account'
            message = render_to_string('core/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return redirect('registration_complete')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'core/registration_complete.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_super_admin() or user.is_admin():
                    return redirect(reverse('admin_dashboard'))
                elif user.is_reviewer():
                    return redirect(reverse('reviewer_dashboard'))
                else:
                    return redirect(reverse('user_dashboard'))
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_super_admin() or user.is_admin():
#                 return redirect(reverse('admin_dashboard'))
#             elif user.is_reviewer():
#                 return redirect(reverse('reviewer_dashboard'))
#             else:
#                 return redirect(reverse('user_dashboard'))
#         else:
#             # Handle invalid login
#             return render(request, 'core/login.html', {'error': 'Invalid username or password'})
#     return render(request, 'core/login.html')

# User Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')