from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(EventUser)
admin.site.register(TaskState)
admin.site.register(EventTask)
admin.site.register(EventTaskReport)
