from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AdvisorBooking
# Register your models here.


class UserAdmin(UserAdmin):
    model = User
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(AdvisorBooking)
