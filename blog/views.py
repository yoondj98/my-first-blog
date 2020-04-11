from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password #패스워드에 대한 부호화를 위해 사용

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
"""
def register(request):
    if request.method == "GET":
        return render(request, 'blog/register.html')
    elif request.method == "POST":
        #여기에 회원가입 처리 코드
        #username = request.POST.['username']
        #password = request.POST['password']
        #re_password = request.POST['re-password']

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)
        useremail = request.POST.get('useremail', None)

        res_data = {} #프론트에 던져줄 응답 데이터
        #모든 값을 입력해야 합니다.
        if not (username and password and re_password and useremail): #None은 False로 인식식
           res_data['error']= "모든 값을 입력해야 합니다."
        #다르면 return
        if password != re_password:
            res_data['error'] = "비밀번호가 다름"
        else:
        #위 정보들로 인스턴스 생성
            fuser = Fuser(
                username = username,
                password = make_password(password),
                useremail = useremail,
            )
            #저장
            fuser.save()

        return render(request, 'blog/register.html', res_data)

def x_login(request):
    if request.method == "GET":
        return render(request, 'x_login.html')
    elif request.method == "POST":
        #전송받은 이메일 비번 확인
        username = request.POST.get('username')
        password = request.POST.get('password')

        #유효성 처리
        res_data ={}
        if not(username and password):
            res_data['error'] ="모든 칸을 다 입력해주세요."
        else:
            #기존(DB)에 있는 Fuser모델과 같은 값인 걸 가져온다.
            fuser = Fuser.objects.get(username=username)# (필드명 = 값)

            #비번이 맞는지 확인. 위에 check_password참조
            if check_password(password, fuser.password):
                #응답 데이터 세션에 값 추가, 수신측 쿠키에 저장됨
                request.session['user'] = fuser.id

                #리다이렉트
                return redirect('home/')
            else:
                res_data['error'] = "비밀번호가 틀렸습니다."

        return render(request, 'blog/x_login.html', res_data) #응답 데이터 res_data 전달달


def x_logout(request):
    if request.session['user']: #로그인 중이라면
        del(request.session['user'])

    return redirect('home/') #홈으로 돌아감.


def home(request):
    user_pk = request.session.get('user') #login함수에서 추가해준 request.session['user'] = fuser.id

    if user_pk: #세션에 user_pk정보가 존재하면
        fuser = Fuser.objects.get(pk = user_pk)
        return HttpResponse(fuser.username) #해당 유저의 Fuser모델의 username 전달

    return HttpResponse("로그인 성공") #세션에 유저 정보 없으면 그냥 home으로
"""