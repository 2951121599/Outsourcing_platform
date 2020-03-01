from django.core.paginator import Paginator
from django.http import *
from django.shortcuts import render, redirect
from outsource.models import *
from functions.decorators import login_required
from django.urls import reverse


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
    '''
    # 3.按照项目预算搜索
    budget = request.GET.get('budget', '')
    # budget = Projects.objects.extra(select={'budget': 'budget+0'})
    # print('*' * 100, type(budget))
    if budget == '1000':
        all_projects = Projects.objects.extra(select={'budget': 'budget+0'}).extra(order_by=["-budget"]).filter(
            budget__range=(0, 1000))
    elif budget == '5000':
        all_projects = Projects.objects.extra(select={'budget': 'budget+0'}).extra(order_by=["-budget"]).filter(budget__range=(1000, 5000))
    elif budget == '10000':
        all_projects = Projects.objects.filter(budget__range=(5000, 10000))
    else:
        all_projects = all_projects.all()
    '''
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
    # projects_top10 = Projects.objects.order_by('budget')

    # 按照项目类别分类
    obj = Projects.objects.all().values("kind")

    # 用户收藏
    user = request.session.get("passport_id")
    u_project_id = Collection.objects.filter(user_id=user)
    collected_list = []
    for obj in u_project_id:
        collected_list.append(obj.projects_id_id)

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

    # 推荐项目 2个相同类别的 不包含本身
    project_kind = project.kind
    recommend_projects = Projects.objects.filter(kind=project_kind).exclude(id=projects_id)[:2]
    return render(request, 'outsource/projects_detail.html', locals())


# 开发者列表页
def developers(request):
    if request.method == 'GET':
        return render(request, 'outsource/developers.html')


# 开发者详情页
def developers_detail(request, developers_id):
    return render(request, 'outsource/developers_detail.html')


# 项目发布
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


# 返回成功的JsonResponse
def SuccessResponse(code):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
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

    # print('is_collect***********', is_collect)  # true
    # print('projects_id***********', projects_id)  # 1
    # print('user***********', user)  # 1
    # 处理数据
    if is_collect == 'True':
        # 要收藏
        collection, created = Collection.objects.get_or_create(projects_id_id=projects_id, user_id=user)
        if created:
            # 未收藏过 进行收藏
            Collection.objects.get(projects_id_id=projects_id, user_id=user)
            return SuccessResponse(200)
        else:
            # 已收藏过 不能重复收藏
            return ErrorResponse(402, '已收藏过 不能重复收藏')
    else:
        # 要取消收藏
        if Collection.objects.filter(projects_id_id=projects_id, user_id=user).exists():
            # 有收藏过 取消收藏
            collection = Collection.objects.get(projects_id_id=projects_id, user_id=user)
            collection.delete()
            return SuccessResponse(201)
        else:
            # 没有收藏过 不能取消
            return ErrorResponse(403, '没有收藏过 不能取消')


# 竞标
def jingbiao(request):
    project_id = request.GET.get('project_id')
    user_id = request.GET.get('user')
    print('project_id', project_id, 'user_id', user_id)
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
