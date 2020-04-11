from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == "GET":
        return render(request, 'accounts/signup.html')
    elif request.method == "POST":

        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)

        res_data ={} #프론트에 던져줄 응답 데이터

        #모든 값을 입력해야됨
        if not( username and password and re_password): #None은 False로 인식
            res_data['error']="모든 값을 입력해야합니다."
            return render(request, 'accounts/signup.html',res_data)
        #비밀번호가 다르면 리턴
        elif User.objects.filter(username = username).exists():
            res_data['error']="이미 존재하는 아이디입니다."
            return render(request, 'accounts/signup.html',res_data)
        elif password != re_password:
            # return HttpResponse("비밀번호가 다름")
            res_data['error']="비밀번호가 다름니다"
            return render(request, 'accounts/signup.html',res_data)
        #같으면 저장
        else : 
            #위 정보들로 인스턴스 생성
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password"])
            auth.login(request,user)
            return render(request,'accounts/signup_success.html')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')