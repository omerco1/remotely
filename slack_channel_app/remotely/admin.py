from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Channel_Member)
admin.site.register(Channel)
admin.site.register(Users)
admin.site.register(Message)