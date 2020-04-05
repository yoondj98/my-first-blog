from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comment)


class FuserAdmin(admin.ModelAdmin): #admin의 ModelAdmin 클래스를 상속
    # pass 상속만 받아 새로운 클래스를 생성
    list_display = ('username', 'password', 'useremail') #admin 페이지에서 뜨도록 사용하는 코드


admin.site.register(Fuser, FuserAdmin) #admin 페이지에 등록