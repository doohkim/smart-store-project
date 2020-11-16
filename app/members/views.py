from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView, \
    GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from members.models import KIUser
from members.serializers.user import KIUserSignupSerializer, KIUserInfoSerializer, \
    KIUserKoenSerializer
from members.text import message


class KIUserCreateAPIView(CreateAPIView):
    serializer_class = KIUserSignupSerializer
    queryset = KIUser.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        # serializer 검증
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # 토큰 생성
            token, _ = Token.objects.get_or_create(user=user)

            # email 토큰 보내
            message_data = message('127.0.0.1:8000', user.pk, token)
            mail_title = "이메일 인증을 완료해 주세요"
            mail_to = user.email
            email = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            # token, user 정보 data
            data = {
                'token': token.key,
                "user": self.serializer_class(user).data
                # 'user': KIUserSignupSerializer(user).data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# retrieve
# get_queryset 필요함
# filter object를 잡아야 한다.
class KIUserActivateAPIView(RetrieveAPIView):
    serializer_class = KIUserInfoSerializer
    queryset = KIUser.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self):

        pk = self.kwargs['pk']
        try:
            if pk is not None:
                obj = self.queryset.get(pk=pk)
        except Exception as ex:
            print('not found user pk from email link to verify user', ex)
        return obj

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        # url token 과 db token 비교
        token_from_email = self.kwargs['token']
        token_check = Token.objects.get(key=token_from_email)
        token_from_db, _ = Token.objects.get_or_create(user=obj)
        if token_from_db != token_check:
            return Response({"your token has problem. It's not match"})

        # 아이디 활성화 시킴
        serializer = self.serializer_class(obj, data={"is_active": True}, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Email verify successfully',
                "user": self.serializer_class(user).data,
                # 'serializer': serializer.data
            }
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            return Response({'the data is not correct'}, status=status.HTTP_400_BAD_REQUEST)


class KIUserLoginAPIView(ListCreateAPIView):
    queryset = KIUser.objects.all()
    serializer_class = KIUserInfoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return KIUser.objects.filter(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        # data = json.loads(request.body.decode('utf-8'))
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:

            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                    'user': KIUserInfoSerializer(user).data
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:

            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class SUBKIUserLoginAPIView(GenericAPIView):
    queryset = KIUser.objects.all()
    serializer_class = KIUserKoenSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, auth=serializer.data)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                data = {
                    "token": token.key,
                    "user": KIUserInfoSerializer(user).data,
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response({'로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)


class KIUserLogoutAPIVIew(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        print(request.user)
        request.user.auth_token.delete()
        return Response({'로그아웃 됨'}, status=status.HTTP_200_OK)
