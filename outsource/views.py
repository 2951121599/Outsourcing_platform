from django.core.paginator import Paginator
from django.http import *
from django.shortcuts import render, redirect
from outsource.models import KindChoice, LanguageChoice, Projects, News
from outsource.models import *
from functions.decorators import login_required
from django.urls import reverse
import json

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
    # 查询每种项目类型的5个最新    和４个最多浏览的信息
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
    # print('当前对象的总个数是:', paginator.count)
    # print('当前对象的面码范围是:', paginator.page_range)
    # print('总页数是：', paginator.num_pages)
    # print('每页最大个数:', paginator.per_page)
    cur_page = request.GET.get('page', 1)  # 得到默认的当前页
    page_obj = paginator.page(cur_page)
    # print('locals--------------', locals())
    # 右侧展示
    # Projects.objects.order_by('?')[:2]
    # 定义上下文
    obj = Projects.objects.all().values("kind")
    # print("obj******************", obj)  # obj****************** <QuerySet [{'kind': 4}]>

    user = request.session.get("passport_id")
    u_project_id = Collection.objects.filter(user_id=user)
    collected_list = []
    for obj in u_project_id:
        collected_list.append(obj.projects_id_id)

    return render(request, 'outsource/projects.html', locals())


# 项目搜素列表页
def projects_list(request, kind, page):
    # 获取排序方式
    sort = request.GET.get('sort', 'default')
    # 判断type_id是否合法
    if int(kind) not in PROJECTS_TYPE.keys():
        return redirect(reverse('outsource:index'))
    # 根据种类id和排序方式查询商品
    projects_li = Projects.objects.get_projects_by_type(kind=kind, sort=sort)
    for i in projects_li:
        print("*" * 30)
        print(i)

    # 分页
    paginator = Paginator(projects_li, 1)
    # 获取分页后的总页数
    num_pages = paginator.num_pages
    # 获取第page页的数据
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)
    projects_li = paginator.page(page)

    # 页码控制
    # 1.总页数<5, 显示所有页码
    # 2.当前页是前3页，显示1-5页
    # 3.当前页是后3页，显示后5页 10 9 8 7
    # 4.其他情况，显示当前页前2页，后2页，当前页
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif num_pages <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)

    # 新品推荐
    projects_new = Projects.objects.get_projects_by_type(kind=kind, limit=2, sort='new')
    # 定义上下文
    type_title = PROJECTS_TYPE[int(kind)]
    context = {
        'projects_li': projects_li,
        'projects_new': projects_new,
        'kind': kind,
        'sort': sort,
        'type_title': type_title,
        'pages': pages
    }

    # 使用模板
    return render(request, 'outsource/projects_list.html', context)


# /detail/projects_id
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


def developers_detail(request, developers_id):
    return render(request, 'outsource/developers_detail.html')


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


def help_menu(request):
    return render(request, 'outsource/help.html')


def guide1(request):
    return render(request, 'outsource/guide1.html')


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


def SuccessResponse(code):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


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
