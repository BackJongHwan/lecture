# main/models.py
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

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
    file = models.FileField(upload_to='lecture_materials/')
    
    def __str__(self):
        return self.file.name
