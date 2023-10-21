from django.http import HttpRequest
from django.views.generic.base import View, TemplateResponseMixin
from django.shortcuts import redirect, get_object_or_404

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from ..models import Module

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    
    def get(self, request: HttpRequest, module_id: int):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    
    def post(self, request: HttpRequest):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
            
        return self.render_json_response({'saved': 'OK'})