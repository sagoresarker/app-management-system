from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .forms import ApplicationForm
from .models import Application

User = get_user_model()

@login_required
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'applications/submit_application.html', {'form': form})

def application_success(request):
    return render(request, 'applications/application_success.html')

@login_required
def user_dashboard(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applications/user_dashboard.html', {'applications': applications})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    applications = Application.objects.all()
    reviewers = User.objects.filter(groups__name='Reviewers')
    return render(request, 'applications/admin_dashboard.html', {'applications': applications, 'reviewers': reviewers})

@user_passes_test(lambda u: u.groups.filter(name='Reviewers').exists())
def reviewer_dashboard(request):
    applications = Application.objects.filter(reviewer=request.user)
    return render(request, 'applications/reviewer_dashboard.html', {'applications': applications})

@user_passes_test(lambda u: u.is_staff)
def assign_reviewer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if reviewer_id:
            reviewer = get_object_or_404(User, id=reviewer_id)
            application.reviewer = reviewer
            application.status = 'under_review'
            application.save()
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.groups.filter(name='Reviewers').exists())
def review_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, reviewer=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            application.status = status
            application.save()
    return redirect('reviewer_dashboard')