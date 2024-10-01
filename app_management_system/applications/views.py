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
from django.contrib import messages

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
@user_passes_test(lambda u: u.is_admin() or u.is_super_admin())
def assign_reviewer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        new_reviewer_email = request.POST.get('new_reviewer_email')

        if reviewer_id:
            reviewer = get_object_or_404(User, id=reviewer_id)
        elif new_reviewer_email:
            reviewer, created = User.objects.get_or_create(
                email=new_reviewer_email,
                defaults={'username': new_reviewer_email, 'role': 'reviewer'}
            )
            if created:
                password = User.objects.make_random_password()
                reviewer.set_password(password)
                reviewer.save()
                send_credentials_email(reviewer, password)
        else:
            return redirect('admin_dashboard')

        application.reviewer = reviewer
        application.status = 'under_review'
        application.save()
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


@login_required
@user_passes_test(lambda u: u.is_user())
def application_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    # Get all relevant fields except 'id', 'user', 'submission_date', etc.
    fields_with_values = [
        {'verbose_name': field.verbose_name, 'value': field.value_from_object(application)}
        for field in application._meta.fields
        if field.name not in ['id', 'user', 'submission_date', 'status', 'reviewer']
    ]

    return render(request, 'applications/application_detail.html', {'application': application, 'fields_with_values': fields_with_values})


@login_required
@user_passes_test(lambda u: u.is_reviewer())
def reviewer_dashboard(request):
    applications = Application.objects.filter(reviewer=request.user)
    return render(request, 'applications/reviewer_dashboard.html', {'applications': applications})

@login_required
@user_passes_test(lambda u: u.is_reviewer())
def application_detail_reviewer(request, application_id):
    application = get_object_or_404(Application, id=application_id, reviewer=request.user)

    # Get all relevant fields except 'id', 'user', 'submission_date', etc.
    fields_with_values = [
        {'verbose_name': field.verbose_name, 'value': field.value_from_object(application)}
        for field in application._meta.fields
        if field.name not in ['id', 'user', 'submission_date', 'status', 'reviewer']
    ]

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            application.status = status
            application.save()
            return redirect('reviewer_dashboard')

    return render(request, 'applications/application_detail_reviewer.html', {
        'application': application,
        'fields_with_values': fields_with_values
    })


@login_required
@user_passes_test(lambda u: u.is_admin())
def application_detail_admin(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Get all relevant fields except 'id', 'user', 'submission_date', etc.
    fields_with_values = [
        {'verbose_name': field.verbose_name, 'value': field.value_from_object(application)}
        for field in application._meta.fields
        if field.name not in ['id', 'user', 'submission_date', 'status', 'reviewer']
    ]

    return render(request, 'applications/application_detail_admin.html', {
        'application': application,
        'fields_with_values': fields_with_values
    })

@login_required
@user_passes_test(lambda u: u.is_user())
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if application.status != 'pending':
        messages.error(request, "You can only edit pending applications.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated successfully.")
            return redirect('user_dashboard')
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'applications/edit_application.html', {'form': form, 'application': application})