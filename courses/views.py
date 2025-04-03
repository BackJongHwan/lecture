from django.db import transaction
from django.shortcuts import render, redirect
from .models import Course, LectureMaterials, File
from .forms import LectureMaterialsForm

# AI를 통해 파일에서 course와 title을 추출하는 예시 함수
def process_file_for_course_title(file_obj):
    # 실제 AI 로직을 여기에 구현합니다.
    # 예시로, 각 파일에 대해 course와 title을 결정합니다.
    extracted_course = "자동 처리 Course"  
    extracted_title = "자동 처리 Title"
    return extracted_course, extracted_title

def upload_lecture_materials(request):
    if request.method == 'POST':
        form = LectureMaterialsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 업로드된 파일 목록을 폼에서 가져옴
                    files = form.cleaned_data.get('files')
                    if files:
                        # 각 파일마다 개별적으로 처리
                        for f in files:
                            # 파일별로 AI 처리를 통해 course와 title 추출
                            extracted_course, extracted_title = process_file_for_course_title(f)
                            # Course 객체를 가져오거나 없으면 생성
                            course_obj, created = Course.objects.get_or_create(name=extracted_course)
                            # 각 파일마다 LectureMaterials 객체를 생성
                            lecture_material = LectureMaterials(course=course_obj, title=extracted_title)
                            lecture_material.save()
                            
                            # 파일 객체 생성 및 저장 후 LectureMaterials와 연결
                            file_instance = File(file=f)
                            file_instance.save()
                            lecture_material.files.add(file_instance)
                return redirect('upload_lecture_materials')
            except Exception as e:
                form.add_error(None, "파일 업로드 중 오류가 발생했습니다. 다시 시도해 주세요.")
    else:
        form = LectureMaterialsForm()
    return render(request, 'upload_lecture_materials.html', {'form': form})

def list_uploaded_files(request):
    # File 모델의 모든 인스턴스를 조회합니다.
    files = File.objects.all()
    return render(request, 'list_uploaded_files.html', {'files': files})