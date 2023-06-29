from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'), # 리뷰 조회 페이지
    path('upload/', views.upload, name='upload'), # 리뷰 입력 페이지
    path('detail/<int:post_id>', views.detail, name='detail'), # 리뷰 상세보기 페이지
    path('detail/<int:post_id>/edit/', views.update, name='edit'), # 리뷰 수정 페이지
    path('detail/<int:post_id>/delete/', views.delete, name='delete'), # 리뷰 삭제 페이지
    path('login/',views.login_view, name='login'), # 로그인 페이지
    path('register/', views.register, name='register'), # 회원가입 페이지
    path('delete-account/', views.deleteaccount, name='deleteaccount'), # 회원탈퇴 페이지
    path('logout/', views.logout_view, name='logout'), # 로그아웃 페이지
]