from django.urls import path
from . import views

from .views import views_courses, views_content, views_modules

urlpatterns = [
    
    # URLS de Cursos:
    
     path('',
         views_courses.ManageCourseListView.as_view(),
         name='manage_course_list'),
    
     path('create/',
         views_courses.CourseCreateView.as_view(),
         name='course_create'),
    
     path('<pk>/edit/',
         views_courses.CourseUpdateView.as_view(),
         name='course_edit'),
    
     path('<pk>/delete/',
         views_courses.CourseDeleteView.as_view(),
         name='course_delete'),
    
     path('<pk>/module',
         views_courses.CourseModuleUpdateView.as_view(),
         name='course_module_update'),
    
    # URLS de Contenido:
    
     path('module/<int:module_id>/content/<model_name>/create/',
          views_content.ContentCreateUpdateView.as_view(),
          name='module_content_create'),
     
     path('module/<int:module_id>/content/<model_name>/<id>/',
          views_content.ContentCreateUpdateView.as_view(),
          name='module_content_update'),
     
     path('content/<int:id>/delete',
          views_content.ContentDeleteView.as_view(),
          name='module_content_delete'),
     
     path("content/order/", 
          views_content.ContentOrderView.as_view(), 
          name="content_order"),
     
    # URLS de Modulos:
    
     path("module/<int:module_id>/", 
          views_modules.ModuleContentListView.as_view(), 
          name="module_content_list"),
     
     path("module/order/", 
          views_modules.ModuleOrderView.as_view(), 
          name="module_order"),
     
]


