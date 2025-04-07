# main/models.py
from django.db import models
import os

class Course(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'course'
        verbose_name = '강의'
    def __str__(self):
        return self.name


class LectureMaterials(models.Model):
    # 강의 자료 모델
    MATERIAL_TYPE_CHOICES = (
        ('lecture', '강의자료'),
        ('exam', '족보'),
        ('assignment', '과제'),
        ('other', '기타'),
    )
    course = models.ForeignKey(
        Course,
        related_name='materials',
        on_delete=models.CASCADE,
        null=True,          # null 값을 허용
        blank=True          # 폼에서 빈 값 허용
    )
    title = models.CharField(max_length=100)
    # course와 title은 AI 처리 후 자동으로 채워지므로 사용자에게 입력받지 않습니다.
    class Meta:
        db_table = 'lecture_materials'
        verbose_name = '강의 자료'
        verbose_name_plural = '강의 자료'
        ordering = ['course']
    def __str__(self):
        return self.title
    # 강의자료, 족보, 과제등으로 나눔
    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPE_CHOICES,
        default='other'  # 기본값은 강의자료
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    file = models.FileField(upload_to='materials/')
    lecture_material = models.ForeignKey(
        LectureMaterials,
        related_name='files',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.file.name
    def delete(self, *args, **kwargs):
        # 서버의 파일 시스템에서 파일 삭제
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # 데이터베이스에서 객체 삭제
        super().delete(*args, **kwargs)