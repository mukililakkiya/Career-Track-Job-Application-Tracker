
from django.contrib import admin
from django.urls import path
from jobapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('add-job/', views.add_job, name='add_job'),

    path('edit-job/<int:id>/', views.edit_job, name='edit_job'),

    path('delete-job/<int:id>/', views.delete_job, name='delete_job'),

    path('register/', views.register_user, name='register'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),
]

