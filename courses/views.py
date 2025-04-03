# main/views.py
from django.shortcuts import render, redirect
from .models import Course, LectureMaterials, File
from .forms import LectureMaterialsForm

def upload_lecture_materials(request):
    if request.method == 'POST':
        form = LectureMaterialsForm(request.POST, request.FILES)
        if form.is_valid():
            lecture_materials = form.save(commit=False)
            lecture_materials.save()  # 강의 자료 저장

            # 여러 파일을 하나씩 처리하여 File 모델에 저장 후 연결
            for f in request.FILES.getlist('files'):
                file_instance = File(file=f)
                file_instance.save()  # 파일 모델에 저장
                lecture_materials.files.add(file_instance)  # LectureMaterials와 파일 연결

            return redirect('upload_lecture_materials')  # 업로드 후 다시 해당 페이지로 리디렉션
    else:
        form = LectureMaterialsForm()

    return render(request, 'upload_lecture_materials.html', {'form': form})
