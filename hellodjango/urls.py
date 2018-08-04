"""hellodjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from demo import views


urlpatterns = [
    path('', views.login),
    # 进首页 - login
    path('login/', views.login),
    path('register/', views.register),
    # 检查用户名
    path('check/', views.check_username),
    # path 函数是在django2中添加进来的 不给资源进入首页
    # index为url的名字
    path('subjects/', views.show_subjects, name='sub'),
    # 需要一个int类型的no, 这个url对应show_teachers这个视图
    path('subjects/<int:no>/', views.show_teachers),
    # good/bad 请求同一个函数make_comment
    path('good/<int:no>/', views.make_comment),
    path('bad/<int:no>/', views.make_comment),
    path('admin/', admin.site.urls),
    # 正则表达式
    # url(r'^$', views.home),
    # url(r'^admin/', admin.site.urls),
    # django1写法 - 命名捕获组 - r是原始字符串 - \d+表示一位或者多位数字
    # url(r'subjects/(?P<no>\d+')
]
