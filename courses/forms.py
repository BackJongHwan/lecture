# main/forms.py
from django import forms
from .models import LectureMaterials

class LectureMaterialsForm(forms.ModelForm):
    class Meta:
        model = LectureMaterials
        fields = ['course', 'title']
        
    # 여기서 `multiple` 속성은 HTML에서 추가합니다.
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)