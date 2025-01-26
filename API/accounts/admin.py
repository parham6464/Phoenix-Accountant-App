from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model

from .forms import CustomChangeForm , CustomCreationForm
from .models import *

# Register your models here.


class CustomAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('lisence',)
        }),
    )


admin.site.register(CustomUser , CustomAdmin)


admin.site.register(GetToken)
admin.site.register(Hesabha)
admin.site.register(Moein)
admin.site.register(tafsili)

admin.site.register(Category)
admin.site.register(Asnad)

admin.site.register(Docs)