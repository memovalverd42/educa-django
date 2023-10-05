from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from typing import TypeVar, Iterable

T = TypeVar('T')

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields: Iterable=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
        
    def pre_save(self, model_instance: T, add: bool):
        
        if getattr(model_instance, self.attname) is None:
            # no hay valor actual
            try:
                qs: QuerySet = self.model.objects.all()
                if self.for_fields:
                    # filtrar por objetos con el mismo valor
                    # por cada campo
                    query = {field: getattr(model_instance, field)\
                        for field in self.for_fields}
                    
                    qs = qs.filter(**query)
                    
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)