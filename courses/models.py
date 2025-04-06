# main/models.py
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'course'
        verbose_name = '강의'
    def __str__(self):
        return self.name


class LectureMaterials(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='materials',
        on_delete=models.CASCADE,
        null=True,          # null 값을 허용
        blank=True          # 폼에서 빈 값 허용
    )
    title = models.CharField(max_length=100)
    files = models.ManyToManyField('File', related_name='lectures')
    
    def __str__(self):
        return self.title

class File(models.Model):
    file = models.FileField(upload_to='materials/')
    
    def __str__(self):
        return self.file.name

class ExamMaterials(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='exam_materials',
        on_delete=models.CASCADE,
        null=True,          # null 값을 허용
        blank=True          # 폼에서 빈 값 허용
    )
    title = models.CharField(max_length=100)
    files = models.ManyToManyField('File', related_name='exam_lectures')
    
    def __str__(self):
        return self.title

class AssignmentMaterials(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='assignment_materials',
        on_delete=models.CASCADE,
        null=True,          # null 값을 허용
        blank=True          # 폼에서 빈 값 허용
    )
    title = models.CharField(max_length=100)
    files = models.ManyToManyField('File', related_name='assignment_lectures')
    
    def __str__(self):
        return self.title