from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from Reviews.models import Review_Models
from .forms import FileUploadForm

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
        return render(request, self.template_name, {'reviews':reviews})

# 리뷰 작성 페이지 로직
def upload(request):
    ### 사용자가 폼을 통해 입력을 했을 경우, 
    if request.method == 'POST':

        # 입력값 받아오기
        title = request.POST['title']
        ratings = request.POST['ratings']
        content = request.POST['content']
        img = request.FILES["imgfile"]

        # 새로운 데이터 생성
        new_file = Review_Models(
            title = title,
            ratings = ratings,
            content = content,
            imgfile = img
        )

        # 입력받은 데이터를 데이터베이스에 저장 -> 자동으로 id 생성
        new_file.save()

        # 결과보기 페이지에 id 값 같이 넘겨주기
        return redirect('detail', post_id=new_file.id)
    
    ### 사용자가 입력하기 전, 폼을 화면에 출력해주는 것
    else:
        fileuploadForm = FileUploadForm()
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'Reviews/review_upload.html', context)
    
def detail(request, post_id):
    review = Review_Models.objects.get(id=post_id)
    return render(request, 'Reviews/review_detail.html', {'review':review})