from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, LoginForm, ApplicationForm, ReviewForm
from .models import Application, Review

def index(request):
    return render(request, 'portal/index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('applications')
    else:
        form = RegisterForm()
    return render(request, 'portal/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('applications')
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def applications_view(request):
    apps = Application.objects.filter(user=request.user)
    review_form = ReviewForm()
    return render(request, 'portal/applications.html', {'applications': apps, 'review_form': review_form})

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            return redirect('applications')
    else:
        form = ApplicationForm()
    return render(request, 'portal/create_application.html', {'form': form})

@login_required
def add_review(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.application = app
            rev.user = request.user
            rev.save()
    return redirect('applications')

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_panel(request):
    apps = Application.objects.all().order_by('-created_at')
    return render(request, 'portal/admin_panel.html', {'applications': apps})

@user_passes_test(is_admin)
def change_status(request, pk):
    if request.method == 'POST':
        app = get_object_or_404(Application, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
    return redirect('admin_panel')
