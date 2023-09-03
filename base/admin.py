from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

admin.site.register(Room) # register the Room model with the admin site
admin.site.register(Topic)
admin.site.register(Message)