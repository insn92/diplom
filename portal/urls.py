from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applications/', views.applications_view, name='applications'),
    path('applications/new/', views.create_application, name='create_application'),
    path('applications/<int:pk>/review/', views.add_review, name='add_review'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('applications/<int:pk>/status/', views.change_status, name='change_status'),
]
