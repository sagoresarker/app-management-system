from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app_management_system.applications.models import Application


# @login_required
# def submit_review(request, application_id):
#     application = get_object_or_404(Application, id=application_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.application = application
#             review.reviewer = request.user
#             review.save()
#             return redirect('dashboard')
#     else:
#         form = ReviewForm()
#     return render(request, 'reviewer/review_form.html', {'form': form, 'application': application})
