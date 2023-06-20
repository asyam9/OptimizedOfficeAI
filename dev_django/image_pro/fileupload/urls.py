from django.urls import path
from .views import fileUpload, result

urlpatterns = [
	path('fileupload/', fileUpload, name="fileupload"),
    path('fileupload/result/<int:post_id>', result, name='result')
    # path('result/', result, name='result')
]