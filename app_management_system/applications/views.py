from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ApplicationForm
from .models import Application
from app_management_system.core.models import CustomUser
import os

User = get_user_model()

from_email_address = os.environ.get('EMAIL_HOST_USER')

@login_required
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            form.save_m2m()
            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'applications/submit_application.html', {'form': form})

def application_success(request):
    return render(request, 'applications/application_success.html')

@login_required
@user_passes_test(lambda u: u.is_user())
def user_dashboard(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applications/user_dashboard.html', {'applications': applications})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_super_admin())
def admin_dashboard(request):
    applications = Application.objects.all()
    reviewers = User.objects.filter(role='reviewer')
    return render(request, 'applications/admin_dashboard.html', {'applications': applications, 'reviewers': reviewers})

@login_required
@user_passes_test(lambda u: u.is_reviewer())
def reviewer_dashboard(request):
    applications = Application.objects.filter(reviewer=request.user)
    return render(request, 'applications/reviewer_dashboard.html', {'applications': applications})

@login_required
@user_passes_test(lambda u: u.is_admin() or u.is_super_admin())
def assign_reviewer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if reviewer_id:
            reviewer = get_object_or_404(User, id=reviewer_id)
            application.reviewer = reviewer
            application.status = 'under_review'
            application.save()

            # Check if it's a new reviewer and send credentials if necessary
            if not reviewer.has_usable_password():
                password = CustomUser.generate_random_password()
                reviewer.set_password(password)
                reviewer.save()
                send_credentials_email(reviewer, password)

            send_assignment_email(reviewer, application)

    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_reviewer())
def review_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, reviewer=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            application.status = status
            application.save()
    return redirect('reviewer_dashboard')

def send_credentials_email(user, password):
    subject = 'Your Account Credentials'
    html_message = render_to_string('core/credentials_email.html', {
        'user': user,
        'password': password,
    })
    plain_message = strip_tags(html_message)
    from_email = from_email_address
    send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

def send_assignment_email(reviewer, application):
    subject = 'New Application Assigned for Review'
    html_message = render_to_string('applications/assignment_email.html', {
        'reviewer': reviewer,
        'application': application,
    })
    plain_message = strip_tags(html_message)
    from_email = from_email_address
    send_mail(subject, plain_message, from_email, [reviewer.email], html_message=html_message)