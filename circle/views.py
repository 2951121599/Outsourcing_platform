from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from circle.models import Questions, Comments
from functions.decorators import login_required

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
        # 存储到数据库
        Questions.objects.create(title=title, content=content, user_id=passport_id)
        return redirect('circle:index')


# /detail/question_id
def question_detail(request, question_id):
    # 根据question_id在数据库中查找是否存在该项目
    id = int(question_id)
    try:
        question = Questions.objects.get(id=id)
        comments = Comments.objects.filter(question_id=id)
    except Exception as e:
        print(e)
        return redirect(reverse('circle:index'))
    return render(request, 'circle/jie/detail.html', locals())


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
    except Exception as e:
        print(e)
        return redirect(reverse('circle:index'))
    return render(request, 'circle/user/home.html', locals())


@login_required
def reply(request):
    if request.method == 'GET':
        return render(request, 'circle/jie/detail.html')
    elif request.method == 'POST':
        comment = request.POST.get('comment')
        question_id = request.GET.get('question_id')
        passport_id = request.session.get('passport_id')
        # 存储到数据库
        Questions.objects.create(comment=comment, question_id=question_id, user_id=passport_id)
        return redirect('circle:detail')
