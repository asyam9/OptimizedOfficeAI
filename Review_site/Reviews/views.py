from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from Reviews.models import Review_Models

# Create your views here.
class IndexView(ListView):
    """리뷰 조회 페이지"""
    model = Review_Models
    template_name = 'Reviews/index.html'
    context_object_name = 'reviews'
    paginate_by = 4 # 한 페이지에 표현할 개수
    ordering = ['-dt_created'] # 순서(- 내림차순)

    def index(self, request):
        reviews = self.model.objects.all()
        return render(request, "Reviews/index.html", {'reviews':reviews})

def upload(request):
    """리뷰 작성 페이지"""
    return HttpResponse("리뷰작성페이지")