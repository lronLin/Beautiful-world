from django.contrib import admin

from demo.models import Teacher, Subject, User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('no', 'username', 'email', 'counter')
    ordering = ('no',)


# 定制管理员界面
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'intro')
    ordering = ('no',)


# 定制模型管理类 - 继承admin下的ModelAdmin管理类
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'intro', 'motto', 'subject', 'manager')
    # 搜索字段
    search_fields = ('name', 'intro')
    # 升序排列
    ordering = ('no', )


# 注册subject
admin.site.register(Subject, SubjectAdmin)
# 注册老师模型 - 管理类
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(User, UserAdmin)

