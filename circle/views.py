from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from circle.models import Questions, Comments
from functions.decorators import login_required
from functions.keywords_filter import DFAFilter

# Create your views here.
from user.models import User


def index(request):
    if request.method != 'GET':
        return HttpResponse("请使用GET请求数据! ")
    questions = Questions.objects.all()
    hot_questions = Questions.objects.all()[:5]
    return render(request, 'circle/index.html', locals())


@login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'circle/jie/add.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        passport_id = request.session.get('passport_id')
        # 关键词过滤
        gfw = DFAFilter()
        path = "./keywords.txt"
        gfw.parse(path)
        content = gfw.filter(content)
        # 存储到数据库
        Questions.objects.create(title=title, content=content, user_id=passport_id)
        return redirect('circle:index')


# /detail/question_id
def question_detail(request, question_id):
    if request.method == 'GET':
        # 根据question_id在数据库中查找是否存在该项目
        id = int(question_id)
        try:
            question = Questions.objects.get(id=id)
            comments = Comments.objects.filter(question_id=id)
        except Exception as e:
            print(e)
            return redirect(reverse('circle:index'))
        return render(request, 'circle/jie/detail.html', locals())


# # submit_comments
# def submit_comments(request, question_id):
#     if request.method == 'POST':
#         # 根据question_id在数据库中查找是否存在该项目
#         id = int(question_id)
#         try:
#             question = Questions.objects.get(id=id)
#             comments = Comments.objects.filter(question_id=id)
#             comment = request.POST.get('comment')
#             passport_id = request.session.get('passport_id')
#             Comments.objects.create(comment=comment, question_id=question_id, user_id=passport_id)
#         except Exception as e:
#             print(e)
#             return redirect(reverse('circle:index'))
#         return render(request, 'circle/jie/detail.html', locals())


# /home/user_id
def home(request, user_id):
    if request.method != 'GET':
        return HttpResponse("请使用GET请求数据! ")
    id = int(user_id)
    print('*' * 50, id)
    try:
        # 获取此用户的所有帖子
        questions = Questions.objects.filter(user_id=id)
        user = User.objects.get(id=user_id)
        # 查询user_id用户的回帖(评论)
        # comments = Comments.objects.filter(user_id=id)
        # for i in comments:
        #     questions_obj = Questions.objects.filter(id=i.id)
        #     for j in questions_obj:
        #         questions_title = Questions.objects.filter(j.title)
        all_comments = Comments.objects.none()
        questions_title = []
        comments = Comments.objects.filter(user_id=id)
        for i in comments:
            questions_obj = Questions.objects.filter(id=i.id)
            questions_title.append(questions_obj)
        for i in questions_title:
            all_comments = all_comments | i
        print('-----------------', all_comments)
        questions_title = chain(all_comments)
        print('-----------------', questions_title)
    #         questions_title = Questions.objects.filter(j.title)

    except Exception as e:
        print(e)
        return redirect(reverse('circle:index'))
    # print(locals())
    return render(request, 'circle/user/home.html', locals())


@login_required
def reply(request):
    referer = request.META.get('HTTP_REFERER', reverse('circle:index'))
    question_id = int(request.POST.get('question_id'))
    comment = request.POST.get('comment', '')
    passport_id = request.session.get('passport_id')
    # 关键词过滤
    gfw = DFAFilter()
    path = "./keywords.txt"
    gfw.parse(path)
    comment = gfw.filter(comment)
    # 存储到数据库
    Comments.objects.create(comment=comment, question_id=question_id, user_id=passport_id)
    return redirect(referer)


def gonggao(request):
    return render(request, 'circle/jie/gonggao.html')
