from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('detail/<int:post_id>/edit/', views.update, name='edit'),
    path('detail/<int:post_id>/delete/', views.delete, name='delete'),
    path('login/',views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('delete-account/', views.deleteaccount, name='deleteaccount'),
    path('logout/', views.logout_view, name='logout'),
    path('viewreview/', views.viewed_reviews, name='viewreview')
]