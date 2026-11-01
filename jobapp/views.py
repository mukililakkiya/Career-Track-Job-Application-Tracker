
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator

from .models import JobApplication
from .forms import JobApplicationForm


@login_required(login_url='login')
def home(request):

    applications = JobApplication.objects.filter(user=request.user)

    # Search
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        applications = applications.filter(
            company_name__icontains=search_query
        )

    if status_filter:
        applications = applications.filter(status=status_filter)

    # Sorting
    sort_by = request.GET.get('sort', '-applied_date')

    allowed_sorting = [
        '-applied_date',
        'applied_date',
        'company_name',
        '-company_name'
    ]

    if sort_by not in allowed_sorting:
        sort_by = '-applied_date'

    applications = applications.order_by(sort_by)

    # Dashboard statistics
    user_applications = JobApplication.objects.filter(user=request.user)

    total_applications = user_applications.count()
    interview_count = user_applications.filter(status='Interview').count()
    selected_count = user_applications.filter(status='Selected').count()
    rejected_count = user_applications.filter(status='Rejected').count()

    # Pagination
    paginator = Paginator(applications, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': page_obj,
        'page_obj': page_obj,
        'total_applications': total_applications,
        'interview_count': interview_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }

    return render(request, 'jobapp/home.html', context)


@login_required(login_url='login')
def add_job(request):

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            return redirect('home')

    else:
        form = JobApplicationForm()

    return render(request, 'jobapp/add_job.html', {
        'form': form
    })


@login_required(login_url='login')
def edit_job(request, id):

    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        form = JobApplicationForm(
            request.POST,
            instance=application
        )

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = JobApplicationForm(instance=application)

    return render(request, 'jobapp/edit_job.html', {
        'form': form
    })


@login_required(login_url='login')
def delete_job(request, id):

    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        application.delete()
        return redirect('home')

    return render(request, 'jobapp/delete_job.html', {
        'application': application
    })


def register_user(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'jobapp/register.html', {
        'form': form
    })


def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'jobapp/login.html', {
        'form': form
    })


def logout_user(request):

    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('home')
