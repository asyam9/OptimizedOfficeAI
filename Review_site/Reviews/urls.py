from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('detail/<int:post_id>/edit/', views.update, name='edit')
]