# course/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('upload/', views.upload_lecture_materials, name='upload_lecture_materials'),
    path('create_course/', views.create_course, name='create_course'),
    path('list_uploaded_files/', views.list_uploaded_files, name='list_uploaded_files'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),   
]

