from django.contrib import admin

# Register your models here.

from ansorapp.models import User,PhoneOTP , Courses
# list_display=('title','content','created_at','updated_at','photos','is_bool')
#     list_display_links=('title','content') #link qib beradi
    # search_fields=('title','content') # search qo'shib beradi
class UserAdmin(admin.ModelAdmin):
    ordering=['id']
    list_display=(
        ['phone']
    )
    search_fields=('phone','date') # search qo'shib beradi

admin.site.register(User,UserAdmin)
admin.site.register(PhoneOTP)
admin.site.register(Courses)
# admin.site.register(Applicants)
