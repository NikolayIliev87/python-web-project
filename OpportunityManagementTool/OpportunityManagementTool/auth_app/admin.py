from django.contrib import admin

from OpportunityManagementTool.auth_app.models import Profile, Manager, OpportunityManagementToolUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(OpportunityManagementToolUser)
class OpportunityManagementToolUserAdmin(admin.ModelAdmin):
    pass