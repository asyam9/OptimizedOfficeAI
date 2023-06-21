from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path('upload/', views.upload, name='upload'),
    path('detail/<int:post_id>', views.detail, name='detail')
]