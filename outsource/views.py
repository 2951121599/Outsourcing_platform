from django.core.paginator import Paginator
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from outsource.models import *
from functions.decorators import login_required
from django.urls import reverse
from itertools import chain
import os


# 主页
def index(request):
    all_news = News.objects.order_by('-id')[:12]
    user = None
    try:
        user = request.session.get("passport_id")
        databases_user_id = Developers.objects.get(user_id=user)
    except Exception as e:
        print(e)
        return render(request, 'outsource/index.html', locals())
    return render(request, 'outsource/index.html', locals())


# 项目列表页
def projects(request):
    # 显示项目 -- 分页 加装饰器(只有GET请求)
    if request.method != 'GET':
        return HttpResponse("请使用GET请求数据! ")

    # 有查询字符串 参考 day04  没有查询字符串的情况下 按照发布时间 降序排序
    all_projects = Projects.objects.filter().order_by("-post_datetime")

    # 1.按照类别分类搜索
    all_kind = KindChoice.objects.all()
    # 取出筛选项目类型
    kind = request.GET.get('kind', '')
    # 在结果集里面做筛选
    if kind:
        all_projects = all_projects.filter(kind=kind)

    # 2.按照开发语言搜索
    all_language = LanguageChoice.objects.all()
    # 取出筛选开发语言类型
    language = request.GET.get('language', '')
    if language:
        all_projects = all_projects.filter(language=language)

    # 查询每种项目类型的5个最新  和４个最多浏览的信息
    app_data_new = Projects.objects.get_projects_by_type(APP, limit=5, sort='new')
    desktop_data_new = Projects.objects.get_projects_by_type(DESK_APP, limit=5, sort='new')
    manage_data_new = Projects.objects.get_projects_by_type(MANAGE_SYSTEM, limit=5, sort='new')
    pc_data_new = Projects.objects.get_projects_by_type(WEBSITE, limit=5, sort='new')
    ui_data_new = Projects.objects.get_projects_by_type(UI, limit=5, sort='new')
    small_program_data_new = Projects.objects.get_projects_by_type(SMALL_PROGRAM, limit=5, sort='new')
    game_data_new = Projects.objects.get_projects_by_type(GAME, limit=5, sort='new')
    other_data_new = Projects.objects.get_projects_by_type(OTHER, limit=5, sort='new')
    # 查询每种项目类型的最多浏览的信息[浏览不常用 以后去掉]
    project_data_hot = Projects.objects.get_projects_by_type(APP, limit=10, sort='hot')

    # 分页
    paginator = Paginator(all_projects, 5)
    cur_page = request.GET.get('page', 1)  # 得到默认的当前页
    page_obj = paginator.page(cur_page)

    # 右侧top10展示 按照预算的高低 存储的是字符串 先转成数字
    projects_top10 = Projects.objects.extra(select={'budget': 'budget+0'})
    projects_top10 = projects_top10.extra(order_by=["-budget"])

    # 按照项目类别分类
    obj = Projects.objects.all().values("kind")

    # 用户收藏
    user = request.session.get("passport_id")
    u_project_id = Collection.objects.filter(user_id=user)
    collected_list = []
    for obj in u_project_id:
        collected_list.append(obj.projects_id_id)

    # 获取当前时间
    from django.utils import timezone
    now = timezone.now()
    import time
    t = int(time.time())
    print("t------------", t)
    # 项目发布时间
    new_publish = []
    for date in all_projects:
        # 得到时间戳
        import datetime
        import time
        # 先把date转变为字符串,然后转换为datetime格式
        this_date = datetime.datetime.strptime(str(date.post_datetime), '%Y-%m-%d %H:%M:%S.%f')
        # 把datetime转变为时间戳
        this_date = time.mktime(this_date.timetuple())
        this_date = int(t - this_date)
        days_5 = int(432000)
        # 5天的时间戳为 432000
        if this_date < days_5:
            new_publish.append(date)
    print("new_publish------------", new_publish)
    return render(request, 'outsource/projects.html', locals())


# 项目详情页
def projects_detail(request, projects_id):
    # 根据projects_id在数据库中查找是否存在该项目
    projects_id = int(projects_id)
    try:
        project = Projects.objects.get(id=projects_id)
    except Exception as e:
        print(e)
        return redirect(reverse('outsource:projects'))

    # 根据project_id从Jingbiao表里面查询竞标人数
    jingbiao_count = len(Jingbiao.objects.filter(project_id=projects_id))
    print('jingbiao_count:', jingbiao_count)
    # 推荐项目 2个相同类别的 不包含本身
    project_kind = project.kind
    recommend_projects = Projects.objects.filter(kind=project_kind).exclude(id=projects_id)[:2]
    user = request.session.get("passport_id")
    try:
        # 当前用户为开发者
        is_developer = Developers.objects.get(user_id=user)
        user = is_developer.user_id
    except Exception as e:
        # 当前用户不是开发者
        user = None
    print('locals:---------', locals())
    return render(request, 'outsource/projects_detail.html', locals())


# 发包方详情页
def publisher_detail(request, publisher_id):
    publisher_id = int(publisher_id)
    print("publisher_id------------", publisher_id)
    try:
        # 获取发包方信息
        user = User.objects.get(id=publisher_id)
        # 获取发包方发布项目的信息
        publisher_projects = Projects.objects.filter(user_id=publisher_id)
        print("publisher_projects------------", publisher_projects)
        return render(request, 'outsource/publisherer_detail.html', locals())
    except Exception as e:
        print('报错信息:', e)
        return redirect(reverse("outsource:projects"))


# 开发者列表页
def developers(request):
    if request.method == 'GET':
        developers = Developers.objects.all()
        return render(request, 'outsource/developers.html', locals())


# 开发者详情页
def developers_detail(request, developers_id):
    developers_id = int(developers_id)
    try:
        # 获取开发者信息
        developer = Developers.objects.get(id=developers_id)
        # 获取承接项目的个数
        confirm_count = len(Confirm.objects.filter(developer_id=developers_id))
        # 信誉积分
        credit_score = confirm_count * 10
        # 评分
        score = Developers.objects.get(id=developers_id).score
        if score == "":
            score = 0
        print("score------------", type(int(float(score))))
        score_int = int(float(score))
        print("score_int------------", score_int)
        # 后端得到多个queryset怎么给前端(困难点)
        all_projects = Projects.objects.none()
        projects_list = []
        # 承接的项目
        confirm_projects = Confirm.objects.filter(developer_id=developers_id)
        for i in confirm_projects:
            projects = Projects.objects.filter(id=i.project_id)
            projects_list.append(projects)
        for i in projects_list:
            all_projects = all_projects | i
        projects_list = chain(all_projects)
        print('****************', projects_list)
        print('------------------', locals())
        return render(request, 'outsource/developers_detail.html', locals())
    except Exception as e:
        print('报错信息:', e)
        return redirect(reverse("outsource:developers"))


# 项目发布
# @csrf_exempt
@login_required
def publish(request):
    if request.method == 'GET':
        all_kind = KindChoice.objects.all()
        print("all_kind--------", all_kind)
        all_language = LanguageChoice.objects.all()
        return render(request, 'outsource/publish.html', locals())
    elif request.method == 'POST':
        # 项目名称 project_name
        print("---------request.POST:", request.POST)
        project_name = request.POST.get('project_name')
        # 项目类别 kind 类似 remember
        kind = request.POST.get('kind', "")
        # 预算 budget
        budget = request.POST.get('budget')
        # 开发语言
        languages = '  '.join(request.POST.getlist('language', ""))
        # 开发周期 cycles
        cycles = request.POST.get('cycles')
        # 项目描述
        project_desc = request.POST.get('project_desc')
        # 创建
        passport_id = request.session.get('passport_id')
        Projects.objects.create(project_name=project_name, kind=kind, budget=budget, language=languages, cycles=cycles,
                                project_desc=project_desc, user_id=passport_id)
        return redirect('outsource:projects')


# 帮助菜单
def help_menu(request):
    return render(request, 'outsource/help.html')


# 需求方帮助
def guide1(request):
    return render(request, 'outsource/guide1.html')


# 接包方帮助
def guide2(request):
    return render(request, 'outsource/guide2.html')


# 开发者注册
@login_required
def reg_dev(request):
    if request.method == 'GET':
        return render(request, 'outsource/reg_dev.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        price_min = request.POST.get('price_min')
        price_max = request.POST.get('price_max')
        work_status = request.POST.get('work_status')
        work_direction = request.POST.get('work_direction')
        language_direction = request.POST.get('language_direction')
        sex = request.POST.get('sex')
        person_introduce = request.POST.get('person_introduce')
        work_experience = request.POST.get('work_experience')
        project_works = request.POST.get('project_works')
        # 创建
        passport_id = request.session.get('passport_id')
        Developers.objects.create(name=name, nickname=nickname, email=email, phone=phone, price_min=price_min,
                                  price_max=price_max, work_status=work_status, work_direction=work_direction,
                                  language_direction=language_direction, sex=sex, person_introduce=person_introduce,
                                  work_experience=work_experience, project_works=project_works, user_id=passport_id)
        return redirect('outsource:projects')


# 返回成功的JsonResponse(不带消息)
def SuccessCodeResponse(code):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
    return JsonResponse(data)


# 返回成功的JsonResponse(带消息)
def SuccessResponse(code, message):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# 返回错误的JsonResponse(不带消息)
def ErrorCodeResponse(code):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    return JsonResponse(data)


# 返回错误的JsonResponse(带消息)
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# 收藏
def collection(request):
    is_collect = request.GET.get("is_collect")
    projects_id = request.GET.get('projects_id')
    user = request.GET.get('user')
    print(projects_id)
    # 处理数据
    if is_collect == 'True':
        # 要收藏
        collection, created = Collection.objects.get_or_create(projects_id_id=projects_id, user_id=user)
        if created:
            # 未收藏过 进行收藏
            Collection.objects.get(projects_id_id=projects_id, user_id=user)
            return SuccessResponse(200, '收藏成功')
        else:
            # 有收藏过 取消收藏
            collection = Collection.objects.get(projects_id_id=projects_id, user_id=user)
            collection.delete()
            return SuccessResponse(201, '取消收藏成功')


# 竞标
def jingbiao(request):
    project_id = request.GET.get('project_id')  # 项目id
    user_id = request.GET.get('user')  # 竞标者id
    project = Projects.objects.get(id=project_id)  # 发包方id
    pub_id = project.user_id
    print('project_id', project_id, 'user_id', user_id, 'pub_id', pub_id)
    # 如果是发包方 不能进行竞标
    if int(pub_id) == int(user_id):
        return ErrorResponse(202, '您是发包方 不能进行竞标!!!')
    else:
        # 先去Jingbiao表中查询  有了就是再次竞标  没有就添加到竞标表中
        jingbiao = Jingbiao.objects.filter(project_id=project_id, user_id=user_id)
        print('jingbiao:', jingbiao)
        if jingbiao:
            # 再次点击竞标    提示不能重复竞标
            return ErrorResponse(201, '不能重复竞标!!!')
        else:
            # 首次竞标  添加到竞标表中
            Jingbiao.objects.create(project_id=project_id, user_id=user_id)
            return SuccessResponse(200)


# 中标
def zhongbiao(request, project_id):
    # 项目状态为 竞标中
    # 项目信息
    try:
        project = Projects.objects.get(id=project_id)
        passport_id = request.session.get('passport_id')
        # 竞标人选
        jingbiao_users = Jingbiao.objects.filter(project_id=project_id)
        jingbiao_count = len(Jingbiao.objects.filter(project_id=project_id))
    except Exception as e:
        print(e)
    return render(request, 'outsource/choose_developer.html', locals())
    # 项目状态为 竞标结束


# 确认开发者
def confirm(request):
    if request.method == 'GET':
        return HttpResponse("请使用POST方式提交数据! ")
    elif request.method == 'POST':
        # 处理数据
        dev_number = int(request.POST.get('dev_number'))
        project_id = request.POST.get('project_id')
        user_id = request.session.get('passport_id')
        print('+' * 100, dev_number, project_id, user_id)
        # 查询用户输入的开发者编号
        jingbiao = Jingbiao.objects.get(id=dev_number)
        user_id2 = jingbiao.user_id
        developer = Developers.objects.get(user_id=user_id2)
        developer_id = developer.id

        # 创建数据 向confirm表添加数据
        try:
            Confirm.objects.create(developer_id=developer_id, project_id=project_id, user_id=user_id)
            # 修改项目状态
            project = Projects.objects.get(id=project_id)
            project.is_Active = False
            project.save()
            # return HttpResponse("开发者选择完毕, 请支付定金后启动项目!!! ")
            return render(request, 'outsource/choose_developer.html', locals())
        except Exception as e:
            print("添加失败! ")
            print(e)
            return HttpResponse("开发者选择 添加失败!!!")


# 合同下载
def file_down(request):
    file_name = "软件开发外包合同.pdf"  # 文件名
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录

    file_path = os.path.join(base_dir, file_name)  # 下载文件的绝对路径
    print(file_path)
    if not os.path.isfile(file_path):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="contract.pdf"'
        print(response)
    except:
        return HttpResponse("Sorry but Not Found the File")

    return response
