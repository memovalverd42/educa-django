from typing import TypeVar

from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, \
     PermissionRequiredMixin
from django.urls import reverse_lazy

from ..models import Course

T = TypeVar('T')

class OwnerMixin:
    def get_queryset(self) -> QuerySet[T]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin:
    def form_valid(self, form: Form) -> HttpResponseRedirect:
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'