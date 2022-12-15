from django.contrib import admin
from .models import posts,comments,likes,follows
# Register your models here.

admin.site.register(posts)
admin.site.register(comments)
admin.site.register(likes)
admin.site.register(follows)