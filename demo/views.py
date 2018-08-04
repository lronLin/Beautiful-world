import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from demo.forms import UserForm
from demo.models import Subject, Teacher, User, proto

# 因为HTTP协议本身是一个无状态协议(不能在两次请求之间保存用户的相关信息)
# 所以服务器为了实现用户跟踪(收到请求时要识别是不是之前访问过的用户)就需要使用其他的辅助方式
# 要实现用户跟踪最常用的手段就是使用Cookie(保存在浏览器中的临时数据)
# 通常我们在Cookie中可以保存一个sessionid(用户跟服务器会话的唯一标识)
# 每次浏览器向服务器发送HTTP请求时会在请求头中携带Cookie(也就是携带了sessionid)
# 服务器通过sessionid就可以确定请求来自之前访问过服务器的哪个用户
# 如果浏览器发起的请求中没有Cookie或者Cookie中没有sessionid的信息
# 那么服务器会认为这是一个新的请求那么会给新的请求分配sessionid并将其写入浏览器
# 如果要清理django_sessions表中掉过期的会话数据可以执行下面的命令
# python manage.py clearsessions


# 进入首页登录
def login(request):
    # get请求进页面, post请求受理表单 - lower()方法
    if request.method.lower() == 'get':
         return render(request, 'demo/login.html', {})
    else:
        username = request.POST['username']
        try:
            user = User.objects.get(username__exact=username)
            password = request.POST['password']
            hasher = proto.copy()
            hasher.update(password.encode('utf-8'))
            if hasher.hexdigest() == user.password:
                # 如果登录成功放一个键login=True(值)
                request.session['user'] = user
                return redirect('sub')
        except User.DoesNotExist:
            pass
        return render(request, 'demo/login.html',
                      {'hint': '用户名或密码错误'})


# 注册
def register(request):
    form = UserForm
    if request.method.lower() == 'get':
        return render(request, 'demo/register.html', {'f': form})

    else:
        ctx = {}
        try:
            # 拿到表单
            form = UserForm(request.POST)
            ctx['f'] = form
            if form.is_valid():
                # 保存与表单对应的模型 - 验证通过 - 保存用户对象
                form.save(commit=True)
                # POST属性 - 类型字典里面装表单数据 - 对应页面的name属性
                # user.username = request.POST['username']
                # user.password = request.POST['password']
                # user.email = request.POST['email']
                # user.save()
                ctx['hint'] = '注册成功请登录!'
                return render(request, 'demo/login.html', ctx)
        except:
            ctx['hint'] = '注册失败, 请重新尝试!'
    return render(request, 'demo/login.html', ctx)


# 检查用户名视图函数
def check_username(request):
    ctx = {}
    # 如果字典里有username
    if 'username' in request.GET:
        # 参数名(后一个username)取到用户名(前一个username)
        username = request.GET['username']
        try:
            # 拿到user对象
            User.objects.get(username__exact=username)
            # 拿得到, 用户名不可用
            ctx['valid'] = False
        except User.DoesNotExist:
            # 拿不到, 用户名可用
            ctx['valid'] = True

    return HttpResponse(json.dumps(ctx),
                        content_type='application/json; charset=utf-8')


def show_subjects(request):
    if 'user' in request.session and request.session['user']:
        # 产生随机编号
        # no = randint(1, 6)
        # 拿到集合 - 拿到指定主键的老师 - :冒号后面的内容就用到了ORM框架
        # list为构造器
        # 字典里键的名字是以后页面取值的名字
        # 通过ORM框架实现持久化操作CRUD
        # ctx = {'teachers_list': list(Teacher.objects.all())}
        # 查所有学科Subject.objects.all()
        ctx = {'subjects_list': Subject.objects.all()}
        return render(request, 'demo/subject.html', ctx)
    else:
        return render(request, 'demo/login.html',
                      {'hint': '请先登录!'})


# 展示老师的方法
def show_teachers(request, no):
    # session中有user, 而且user不为空
    if 'user' in request.session and request.session['user']:
        # 查学科 - pk主键 - 学科反查老师属性teacher_set - 拿到学科的所有老师 - all是学科里的老师
        # teachers = Subject.objects.get(pk=no).teacher_set.all()
        # 查询老师 subject里面的no=no
        # SQL语句 : 'select * from tb_teacher where sno=no'
        # select_related('subject')方法将1 + n --> 连查
        teachers = Teacher.objects.filter(subject__no=no)\
            .select_related('subject')
        # 渲染页面
        ctx = {'teachers_list': teachers}
        return render(request, 'demo/teacher.html', ctx)
    else:
        return render(request, 'demo/login.html',
                      {'hint': '请先登录!'})


# 好评视图函数
def make_comment(request, no):
    # 放入一个字典
    ctx = {'code': 200}
    # session中有user, 而且user不为空
    if 'user' in request.session and request.session['user']:
        # 通过session拿到正在登陆使用的user
        user = request.session['user']
        # counter>0 - 有票
        if user.counter > 0:
            try:
                # 通过编号拿到老师
                teacher = Teacher.objects.get(pk=no)
                # 拿到path - path就是请求的url - '/good/3'
                if request.path.startswith('/good'):
                    teacher.good_count += 1
                    ctx['result'] = f'好评({teacher.gcount})'
                else:
                    # 投一票减一
                    teacher.bad_count += 1
                    ctx['result'] = f'差评({teacher.bcount})'
                teacher.save()
                user.counter -= 1
                # 此处不能使用user.save()来更新user对象
                # 因为save()方法要重新给密码生成SHA1摘要
                User.objects.filter(username__exact=user.username)\
                    .update(counter=user.username)
                # 通过给session中的user重新赋值来强制更新数据库中持久化的session数据
                request.session['user'] = user
                # 捕获老师不存在的异常
            except Teacher.DoesNotExist:
                ctx['code'] = 404
        else:
            ctx['code'] = 403
            ctx['result'] = '票数不足'
    else:
        ctx['code'] = 302
        ctx['result'] = '请先登录'
    return HttpResponse(json.dumps(ctx),
                        content_type='application/json; charset=utf-8')

