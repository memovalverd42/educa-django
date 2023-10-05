from django.db import models

class TimeStampedModel(models.Model):
    '''
    Clase abstracta que provee los campos created y updated
    '''
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True