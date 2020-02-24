from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Project, LikeNum, LikeUser
from functions.decorators import login_required

import redis

# 创建数据库连接对象
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


@login_required
def index(request):
    projects = Project.objects.all()

    # 某用户点赞的所有项目
    user = request.session.get("passport_id")
    user_like_project_id = LikeUser.objects.filter(like_user_id=user)
    like_list = []
    for obj in user_like_project_id:
        like_list.append(obj.project_id)
    return render(request, 'trade/index.html', locals())


def detail(request):
    return render(request, 'trade/detail.html', locals())


# 上传图片功能
def push(request):
    if request.method == 'GET':
        return render(request, 'trade/push.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get("link")
        desc = request.POST.get('desc')
        # 1.获取上传的图片
        share_img = request.FILES['share_img']
        # 2.创建一个新文件
        save_path = '%s/img/%s' % (settings.MEDIA_ROOT, share_img.name)
        with open(save_path, 'wb') as f:
            # 3.获取上传文件的内容并写到创建的文件中
            for content in share_img.chunks():
                f.write(content)
        # 4.在数据库中保存上传记录
        passport_id = request.session.get('passport_id')
        # 存储到数据库
        project = Project.objects.create(title=title, link=link, desc=desc, user_id=passport_id,
                                         image_url='img/%s' % share_img.name)
        LikeNum.objects.create(project_id=project.id, like_num=0)
        # 5.返回
        return redirect('trade:index')


def mine(request):
    if request.method != 'GET':
        return HttpResponse("请使用GET方式请求数据! ")
    else:
        passport_id = request.session.get('passport_id')
        my_projects = Project.objects.filter(user_id=passport_id)
        print("my_projects:--------------------", my_projects)
        return render(request, 'trade/mine.html', locals())


def require(request):
    return render(request, 'trade/require.html', locals())


# 博客文章首页(显示阅读前10的文章)
def topic_index(request):
    # 取出阅读前10的文章
    all_topic = r.zrevrange('topic:read', 0, 9)
    # 查库 id ->title
    for n, t_id in enumerate(all_topic):
        rank = n + 1
        n_t_id = t_id.decode()
        html = "排名: %s , id: %s " % (rank, n_t_id)
        print(html)
    return HttpResponse("这是index页! ")


# 博客文章详情页(增加阅读量)
def topic_detail(request, topic_id):
    cache_key = 'topic:read'
    if r.zrank(cache_key, topic_id) is None:
        # 若没有topic_id的key,则返回值为None
        # 第一次来
        r.zadd(cache_key, {topic_id: 1})
    else:
        # 执行加值操作
        r.zincrby(cache_key, 1, topic_id)
    return HttpResponse("这是第 %s 详情页 " % topic_id)


def SuccessResponse(code, like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
    data['like_num'] = like_num
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like(request):
    is_like = request.GET.get('is_like')
    project_id = request.GET.get('project_id')
    user = request.GET.get('user')

    print("is_like:", is_like, "project_id:", project_id, "user", user)
    # 处理数据
    if is_like == 'True':
        # 要点赞
        like_user, created = LikeUser.objects.get_or_create(like_user_id=user, project_id=project_id)
        print("like_count.like_num:", like_user.like_user_id, "created:", created)
        if created:
            # 未点赞过 进行点赞
            # LikeUser.objects.get_or_create(project_id=project_id, like_user_id=user)
            like_count = LikeNum.objects.get(project_id=project_id)
            print("*" * 50, like_count.like_num)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(200, like_count.like_num)
        else:
            # 已点赞 不能重复点赞
            return ErrorResponse(402, '已点赞 不能重复点赞')
    else:
        # 要取消点赞
        if LikeUser.objects.filter(project_id=project_id, like_user_id=user).exists():
            like_user = LikeUser.objects.filter(project_id=project_id, like_user_id=user)
            # 有点赞过 取消点赞
            like_count = LikeNum.objects.get(project_id=project_id)
            # 数据存在，对数量进行减一
            like_user.delete()
            like_count.like_num -= 1
            like_count.save()
            return SuccessResponse(201, like_count.like_num)
        else:
            # 没有点赞过 不能取消
            return ErrorResponse(403, '没有点赞过 不能取消')
