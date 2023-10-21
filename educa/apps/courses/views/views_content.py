from django.apps import apps
from django.http import HttpRequest
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from django.shortcuts import redirect, get_object_or_404

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from ..models import Module, Content

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'
    
    def get_model(self, model_name: str):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        
        return Form(*args, **kwargs)
    
    def dispatch(self, request: HttpRequest, module_id: int, model_name: str, id: int=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
            
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request: HttpRequest, module_id: int, model_name: str, id: int=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })
        
    def post(self, request: HttpRequest, module_id: int, model_name: str, id: int=None):
        form = self.get_form(self.model,
                           instance=self.obj,
                           data=request.POST,
                           files=request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            
            if not id:
                # nuevo contenido
                Content.objects.create(module=self.module,
                                       item=obj)
            
            return redirect('module_content_list', self.module.id)
        
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })


class ContentDeleteView(View):
    def post(self, request: HttpRequest, id: int):
        content: Content = get_object_or_404(Content,
                                             id=id,
                                             module__course__owner=request.user)
        
        module = content.module
        content.item.delete()
        content.delete()
        
        return redirect('module_content_list', module.id)
    
class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    
    def post(self, request: HttpRequest):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__coruse__owner=request.user) \
                                       .update(order=order)
                                       
        return self.render_json_response({'saved': 'OK'})