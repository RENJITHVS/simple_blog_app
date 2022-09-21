from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Blog


# class UserAdmin(UserAdmin):
    
#     model = User
#     list_display = ('username', 'email','is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('email','username','email','is_staff',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2', 'is_staff',)}
#         ),
#     )
#     search_fields = ('username','email')
#     ordering = ('username',)

# admin.site.register(User, UserAdmin)
admin.site.register(Blog)
