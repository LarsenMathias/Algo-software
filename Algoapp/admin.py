from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(MembershipPlan)

@admin.register(MembershipPlan)
class memberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Blog)
class memberAdmin(admin.ModelAdmin):
    list_display = ['author', 'title']

@admin.register(BusinessDetails)
class memberAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Newsletter_users)
class memberAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(our_clients)
class memberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'question', 'way_to_contact']

@admin.register(free_triel_users)
class memberAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(UserMembership)

