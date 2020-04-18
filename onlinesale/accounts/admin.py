from django.contrib import admin
from django.contrib.auth.models import Group

from .forms import UserAdminCreationForm, UserAdminChangeForm
#we are gonna embedd this forms in the Admin page

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# here we are importing 'UserAdmin' as 'BaseUserAdmin' so that
# we can create our own class by its ('UserAdmin') name 
# and inherit the original one by another name i.e 'BaseUserAdmin'

class UserAdmin(BaseUserAdmin):

    #modification in admin site to update form (any model class)
    form = UserAdminChangeForm
    fieldsets = (
        ('Personal Info',{
            'fields':('full_name','mobile','email','password')
            }
        ),
        ('Permissions',{
            'fields':('admin','staff','active',)
            }
        ),
    )

    #modification in admin site add form (any model class)
    add_form = UserAdminCreationForm
    add_fieldsets = (

        ("User Details",{
            'classes':('wide',),
            'fields':('full_name','mobile','email',)
            }
        ),
        ("Password Details",{
            'classes':('wide',),
            'fields':('password1','password2',)
            }
        )
    )

    #modifications in view page of admin site
    list_filter = ('active','admin','staff')
    filter_horizontal = ()
    ordering = ('full_name',)
    list_display = ('full_name','email')
    search_fields = ('full_name','email','mobile')


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
#since we are not using groups we are simply unregistering it