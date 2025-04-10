# main/forms.py
from django import forms
from multiupload.fields import MultiFileField
from .models import LectureMaterials, Course

class LectureMaterialsForm(forms.ModelForm):
    # 사용자에게 보여질 파일 업로드 필드 (여러 파일 업로드 허용)
    files = MultiFileField(
        min_num=1,  # 최소 1개 이상 업로드
        max_num=100,  
        max_file_size=1024 * 1024 * 100  # 각 파일 최대 100MB 제한
    )
    class Meta:
        model = LectureMaterials
        # course, title은 AI 처리 후 자동으로 채워지므로 사용자에게 입력받지 않습니다.
        fields = []  

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']
        labels = {
            'name': '강좌명',
        }