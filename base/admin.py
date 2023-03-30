from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, Class, India_Abroad

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Class)
admin.site.register(India_Abroad)

