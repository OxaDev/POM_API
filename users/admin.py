from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "email", "joined_date")
admin.site.register(User, UserAdmin)