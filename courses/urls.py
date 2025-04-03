# course/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_lecture_materials, name='upload_lecture_materials'),
]
