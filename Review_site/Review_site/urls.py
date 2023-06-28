from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reviews/', include('Reviews.urls'))
]

# media 파일 요청을 처리하는 방법을 명시(2)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)