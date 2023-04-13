from django.contrib import admin
from app.models import *

# Register your models here.

admin.site.register(User_access)
# admin.site.register(Follow_model)
admin.site.register(Following_model)
admin.site.register(Likes_model)
admin.site.register(Post_model)
admin.site.register(Comment)

