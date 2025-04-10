from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Course, LectureMaterials, File
from .forms import LectureMaterialsForm, CourseForm

# AI를 통해 파일에서 course와 title을 추출하는 예시 함수
def process_file_for_course_title(file_obj):
    # 실제 AI 로직을 여기에 구현합니다.
    # 예시로, 각 파일에 대해 course와 title을 결정합니다.
    extracted_course = "미지정 파일"  
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
                            file_instance = File(file=f, lecture_material=lecture_material)
                            file_instance.save()
                return redirect('main_page')
            except Exception as e:
                form.add_error(None, "파일 업로드 중 오류가 발생했습니다. 다시 시도해 주세요.")
    else:
        form = LectureMaterialsForm()
    return render(request, 'upload_lecture_materials.html', {'form': form})

def list_uploaded_files(request):
    # 미지정 파일 강좌가 없으면 생성
    unassigned_course, created = Course.objects.get_or_create(
        name="미지정 파일",
        defaults={'name': "미지정 파일"}
    )
    
    # 모든 강좌와 미지정 파일을 포함한 구조화된 데이터 준비
    courses = Course.objects.all().order_by('name')
    structured_data = {
        'courses': {},
    }

    # 각 강좌별로 자료 유형에 따라 파일 분류
    for course in courses:
        structured_data['courses'][course.id] = {
            'name': course.name,
            'lecture': [],
            'exam': [],
            'assignment': [],
            'other': []
        }

    # 모든 강의 자료를 순회하며 분류
    lecture_materials = LectureMaterials.objects.select_related('course').prefetch_related('files').all()
    
    # course가 None인 자료들을 미지정 파일 강좌로 이동
    LectureMaterials.objects.filter(course__isnull=True).update(course=unassigned_course)
    
    for material in lecture_materials:
        files = material.files.all()
        if material.course:
            course_data = structured_data['courses'][material.course.id]
            course_data[material.material_type].extend(files)

    # 마지막으로 열린 폴더 정보 전달
    last_opened = {
        'course_id': request.session.get('last_opened_course'),
        'material_type': request.session.get('last_opened_type')
    }

    return render(request, 'list_uploaded_files.html', {
        'structured_data': structured_data,
        'last_opened': last_opened
    })

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # 강좌 목록 페이지 등 원하는 페이지로 리다이렉트
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

def delete_file(request, file_id):
    if request.method == 'POST':
        try:
            file_instance = get_object_or_404(File, id=file_id)
            # 삭제하기 전에 course_id를 저장
            course_id = file_instance.lecture_material.course.id if file_instance.lecture_material and file_instance.lecture_material.course else None
            material_type = file_instance.lecture_material.material_type if file_instance.lecture_material else None
            
            file_instance.delete()  # 모델의 delete 메서드 호출
            
            # 세션에 마지막으로 열린 폴더 정보 저장
            if course_id:
                request.session['last_opened_course'] = course_id
                request.session['last_opened_type'] = material_type
            
            return redirect('list_uploaded_files')
        except Exception as e:
            return redirect('list_uploaded_files')
    return redirect('list_uploaded_files')

def main_page(request):
    files = File.objects.all().order_by('-id')  # 최신 파일부터 정렬
    return render(request, 'main.html', {'files': files})

def delete_course(request, course_id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=course_id)
            
            # "미지정 파일" 강좌는 삭제할 수 없음
            if course.name == "미지정 파일":
                return redirect('list_uploaded_files')
            
            # 강좌에 속한 모든 강의자료의 course를 None으로 설정
            LectureMaterials.objects.filter(course=course).update(course=None)
            
            # 강좌 삭제
            course.delete()
            return redirect('list_uploaded_files')
        except Exception as e:
            return redirect('list_uploaded_files')
    return redirect('list_uploaded_files')

