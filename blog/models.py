from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Fuser(models.Model):  # models.Model를 상속
    username = models.CharField(max_length=32,
                                verbose_name='사용자명'  # admin 페이지에서 보일 컬럼명
                                )
    #5~7을 드래그 한뒤 Alt+Shift+Down하면 편함
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호'  # admin 페이지에서 보일 컬럼명
                                )
    register_dttm = models.DateField(auto_now_add=True, # 자동으로 해당 시간이 추가됨
                                     verbose_name="가입날짜"
                                     )


    #데이터가 문자열로 변환이 될 때 어떻게 나올지(반환해줄지) 정의하는 함수가 __str__이다.
    def __str__(self):
        return self.username


    #별도로 테이블명을 지정하고 싶을 때 쓰는 코드(안해도 됨)
    class Meta:
        db_table = 'user_define_fuser_table' #테이블 명 지정
        verbose_name = '사용자 모임' #노출될 테이블 이름 변경
        verbose_name_plural = '사용자 모임'