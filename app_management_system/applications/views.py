from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import Application


@login_required
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'applications/submit_application.html', {'form': form})

def application_success(request):
    return render(request, 'applications/application_success.html')

@login_required
def dashboard(request):
    user = request.user
    applications = Application.objects.filter(user=user)
    return render(request, 'applications/dashboard.html', {'applications': applications})


@login_required
def assign_reviewer(request, application_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        reviewer_email = request.POST['email']
        try:
            reviewer = User.objects.get(email=reviewer_email)
        except User.DoesNotExist:
            reviewer = User.objects.create_user(username=reviewer_email.split('@')[0], email=reviewer_email, password='temporary_password')
        application.reviewer = reviewer
        application.save()
        return redirect('admin_application_list')
    return render(request, 'applications/assign_reviewer.html', {'application': application})
