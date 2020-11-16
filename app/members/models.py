import datetime

from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

SOCIAL_CHOICES = (
    # 카카오로 가입
    ('kakao', 'Kakao'),
    # 네이 가입
    ('naver', 'Naver'),
    # 구글로 가입
    ('google', 'Google'),
    # 직접 가입
    ('email', 'Email'),
    # 직접
    ('username', 'Username'),
    # 관리자로 가입
    ('admin', 'Admin'),
)

GENDER_CHOICES = (
    # 남성
    ('male', 'Male'),
    # 여성
    ('female', 'Female'),
)


class KIUserManager(UserManager):

    def create_user(self, username, nickname, login_by, email, gender,
                    birth_date, phone, password=None):
        if not username:
            raise ValueError('user must have a username')
        if not email:
            raise ValueError('user must have a email')
        if not nickname:
            raise ValueError('user must have a nickname')
        user = self.model(
            username=username,
            email=email,
            login_by=login_by,
            nickname=nickname,
            phone=phone,
            birth_date=birth_date,
            gender=gender,

        )
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, nickname, phone, email, password=None):
        print('create_super_user')
        user = self.model(
            username=username,
            email=email,
            login_by='admin',
            nickname=nickname,
            phone=phone,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self.db)
        return user


class KIUser(AbstractUser):
    # 로그인 방법
    login_by = models.CharField('로그인 방법', choices=SOCIAL_CHOICES, max_length=20)
    # 보여지는 유저 이름
    nickname = models.CharField('닉네임', max_length=100, unique=True)
    # 이메일
    email = models.EmailField('이메일', unique=True)
    # 핸드폰 번호
    phone = PhoneNumberField(max_length=15, help_text='핸드폰 번호', unique=True, )
    # 생일
    birth_date = models.DateField('생년월일', default=timezone.now)
    # 성별
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default='male')
    # 주소
    address = models.TextField(help_text='주소', default='')
    # 유저 포인트
    point = models.IntegerField('유저 포인트', default=0)
    # 추천 코드
    recommand_code = models.CharField('추천 코드', max_length=30, default='')
    # 회원가입 약관 동의
    clause_agree = models.BooleanField('회원가입 약관 동의', default=True)
    # 마케팅 동의
    marketing_agree = models.BooleanField('마케팅 동의', default=False)
    # Push 동의
    push_agree = models.BooleanField('알람', default=False)
    # 키워드 즐겨찾기
    favorites = models.ManyToManyField(
        'Keyword', through='KeywordFavorite', related_name='users', help_text='키워드 즐겨찾기 좋아요')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname', 'password', 'phone', ]
    objects = KIUserManager()

    def age(self):
        today = datetime.date.today()
        birth = self.birth_date
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.pk} | {self.username} | {self.email}'


class KeywordFavorite(models.Model):
    user = models.ForeignKey(
        KIUser, on_delete=models.CASCADE)
    keyword = models.ForeignKey(
        'Keyword', related_name='keyword_favorite', on_delete=models.CASCADE)

    liked = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.user.name} 의 {self.keyword.name} | 좋아요 {self.liked}'


class Keyword(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(
        KIUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '키워드'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.user.username} | 검색한 키워드 : {self.name}'


@receiver(post_save, sender=KIUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
