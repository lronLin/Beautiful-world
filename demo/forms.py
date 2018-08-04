
from django import forms

from demo.models import User


# 定义表单 - 继承ModelForm - 创建表单对象 - ModelForm定制页面 - widget:小组件-->指表单中的表单控件
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, max_length=20, min_length=6)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)
    email = forms.CharField(widget=forms.EmailInput, max_length=255)

    # 对应模型
    class Meta(object):
        # 绑定User模型
        model = User
        # 用户名与密码邮箱对应
        fields = ('username', 'password', 'email')
