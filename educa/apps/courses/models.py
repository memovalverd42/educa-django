from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from ..core.models import TimeStampedModel
from .fields import OrderField

class Subject(TimeStampedModel):
    """
    Modelo de un Tema para un Curso

    Attributes:
        title (str): El título de la materia.
        slug (str): Una versión amigable para URL del título.

    Meta:
        ordering (list of str): La lista de campos por los que se ordenarán los
        registros de materias (por defecto, se ordenarán por título).

    Methods:
        __str__: Devuelve una representación legible en cadena de la materia.

    """
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self) -> str:
        return self.title

class Course(TimeStampedModel):
    """
    Representa un curso en un sistema educativo.

    Attributes:
        owner (User): El usuario propietario del curso.
        subject (Subject): La materia a la que está asociado el curso.
        title (str): El título del curso.
        slug (str): Una versión amigable para URL del título.
        overview (str): Una descripción general del curso.

    Meta:
        ordering (list of str): La lista de campos por los que se ordenarán los
        registros de cursos (por defecto, se ordenarán por fecha de creación descendente).

    Methods:
        __str__: Devuelve una representación legible en cadena del curso.

    """
    
    owner = models.ForeignKey(User, 
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self) -> str:
        return self.title
    
class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules', 
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    
    class Meta:
        ordering = ['order']
    
    def __str__(self) -> str:
        return f'{self.order}. {self.title}'

class Content(models.Model):
    module = models.ForeignKey(Module, 
                               related_name='contents',
                               on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in':(
                                             'text',
                                             'video',
                                             'image',
                                             'file'
                                         )
                                     })
    
    object_id = models.PositiveIntegerField()
    
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        ordering = ['order']
    
class ItemBase(TimeStampedModel):
    owner = models.ForeignKey(User, 
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    
    class Meta:
        abstract = True
        
    def __str__(self) -> str:
        return self.title
    
    def render(self):
        print(self._meta.model_name)
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )
    
class Text(ItemBase):
    content = models.TextField()
    
class File(ItemBase):
    file = models.FileField(upload_to='files')
    
class Image(ItemBase):
    file = models.FileField(upload_to='images')
    
class Video(ItemBase):
    url = models.URLField()
    
