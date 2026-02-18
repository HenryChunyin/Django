from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from lab01 import models
from django.views.generic import TemplateView


def main(request):
    return HttpResponse("Hello, world. You're at the test")


def person(request):
    # models.Person.objects.create(
    #     name="leichunyin",
    #     age=34,
    #     gender="male"
    #     )

    person = models.Person.objects.all()  # 列表。一行一行的数据(字典)
    # print(person.values())
    for item in person.values():
        print(item.keys(), item.values())
    print(person.last())

    return HttpResponse("successful!")


def depart_list(request):
    '''部门列表'''
    depart = models.Department.objects.all()
    print(depart)

    return render(request, 'depart_list.html', {'depart': depart})


def depart_add(request):
    '''新建部门'''
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取提交过来的数据
    name = request.POST.get('name')  # 获取的是inpu标签中name属性的值，这里是name
    # 保存数据
    models.Department.objects.create(name=name)
    # 重定向会列表
    return redirect('/depart/list/')


def depart_delete(request):
    '''部门删除'''
    # 获取GET请求传来的数据
    nid = request.GET.get('nid')
    # 过滤+删除
    models.Department.objects.filter(id=nid).delete()


def depart_edit(request, nid):
    '''部门编辑'''
    if request.method == 'GET':
        # 过滤取到的是对象列表，.first取出第一个对象
        obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'obj': obj})

    now_obj = request.POST.get('depart_name')
    models.Department.objects.filter(id=nid).update(name=now_obj)
    return redirect('/depart/list/')


def user_list(request):
    '''员工列表'''

    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     # obj.create_time 是datetime类型
    #     print(obj.create_time.strftime('%Y-%m-%d %H:%M:%S'))  # 转换成字符串类型

    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    '''添加员工'''
    if request.method == 'GET':
        context = {
            'gender_choice': models.UserInfo.gender_choices,
            'department_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    name = request.POST.get('name')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    account = request.POST.get('account')
    password = request.POST.get('pwd')
    ctime = request.POST.get('ctime')
    department = request.POST.get('depart')

    models.UserInfo.objects.create(
        name=name, gender=gender, age=age,
        amount=account, password=password, create_time=ctime,
        depart_id=department
    )
    # depart_id是外键的那列id的值，depart是那一行的对象，可以再读取列，depart.name

    return redirect('/user/list/')


########################## ModelForm 设计表单 #####################
from django import forms


# 定义ModelForm类，用于指定数据表和字段
# 即定义一个表单的类
class UserAddModelForm(forms.ModelForm):
    '''员工表单类'''
    # 默认验证提交表达不为空。
    # 增加其他验证在表单类中重写字段的表单类属性。
    password = forms.CharField(min_length=8,  # 重新定义某字段的表单的属性
                               label='密码')  # 要重新定义标签，其他不用

    class Meta:
        model = models.UserInfo  # 指定要调取的数据表
        fields = ['name', 'gender', 'password', 'age', 'amount', 'depart', 'create_time']  # 指定要调取的字段,列表中的字段顺序为展示的顺序
        # widgets={
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'}),
        # }

    # 重写表单初始化方法
    # 批量修改初始化表单时，输入框的widget的属性
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'password':
                field.widget = forms.PasswordInput()
            if name == 'create_time':
                field.widget = forms.DateInput()

            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


# 视图函数实例化表单类，生成表单
# 即：生成“输入框”或者“选择框”等post请求的表单
def user_modelform_add(request):
    '''新增员工'''
    if request.method == 'GET':
        form = UserAddModelForm()
        return render(request, 'model_form_user_add.html', {"form": form})

    form = UserAddModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 此时会拿到字段和输入数据构成的字典。
        form.save()  # 调用ModelForm的save方法，自动保存到类指定的数据表中
        return redirect('/user/list/')

    # print(form.errors)# 见前端{{ field.errors.0 }}
    return render(request, 'model_form_user_add.html', {"form": form})


def user_modelform_edit(request, nid):
    '''员工管理'''
    row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取对应编辑行的对象

    if request.method == 'GET':
        form = UserAddModelForm(instance=row_obj)  # 实例化指定行(对象)的表单对象
        return render(request, 'model_form_user_edit.html', {"form": form})

    # 接收POST请求的数据
    form = UserAddModelForm(data=request.POST, instance=row_obj)
    # 重新实例化指定行(对象)的表单对象，指定数据。
    # 重新实例化表单对象，接收数据，指定赋值的对象。

    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'model_form_user_edit.html', {"form": form})


def user_modelform_delete(request, nid):
    '''员工删除'''
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


############################### 研发管理 ####################################

class ExpPrjModelForm(forms.ModelForm):
    # proj_num = forms.CharField(
    #     label= '项目编号',
    #     validators=[RegexValidator(r'^pj[0-9]{5}$','项目编号以pj开头+5位数字')]
    # )

    class Meta:
        model = models.ExperimentProject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}
            if name == 'proof_time' or name == 'rd_time' or name == 'try_produ_time' or name == 'production_time':
                field.required = False

    # 钩子方法的数据验证
    def clean_proj_num(self):  # 方法名的命名规则：clean_变量名
        t_proj_num = self.cleaned_data['proj_num']  # 获取用户提交的数据

        if len(t_proj_num) < 8:
            raise ValidationError('长度须不少于8个字符')

        return t_proj_num


def expe_list(request):
    form = ExpPrjModelForm()
    expe_obj = models.ExperimentProject.objects.all()

    return render(request, 'lab_templates/experiment_project.html',
                  {'form': form, 'expe_obj': expe_obj})


def expe_add(request):
    if request.method == 'GET':
        form = ExpPrjModelForm()

        return render(request, 'lab_templates/expe_add.html', {'form': form})

    form = ExpPrjModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/lab/expe/list/')
    # print(form.errors)
    return render(request, 'lab_templates/expe_add.html', {'form': form})


def expe_edit(request, nid):
    row_obj = models.ExperimentProject.objects.get(id=nid)
    if request.method == 'GET':
        form = ExpPrjModelForm(instance=row_obj)
        return render(request, 'lab_templates/expe_edit.html', {'form': form})

    form = ExpPrjModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/lab/expe/list/')
    print(form.errors)
    return render(request, 'lab_templates/expe_edit.html', {'form': form})


def expe_record(request):
    return render(request, 'lab_templates/expe_record.html')


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Oder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


def order_list(request):
    form = OrderModelForm()

    return render(request, 'order_list.html', {'form': form})


################## 文件上传 ####################

def upload_files(request):
    '''上传文件'''
    if request.method == 'POST':
        print(
            request.POST,
            request.FILES
        )

    return render(request, 'temp/upload_files.html')


class AboutViews(TemplateView):
    template_name = "order_list.html"


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

'''生成PDF文件
def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
'''

