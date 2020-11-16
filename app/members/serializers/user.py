from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from members.exceptions import PasswordNotMatchingException
from members.models import KIUser


class KIUserSignupSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d'])
    phone = PhoneNumberField()
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = KIUser
        fields = [
            'pk',
            'username',
            'email',
            'nickname',
            'phone',
            'gender',
            'birth_date',
            'address',
            'password1',
            'password2',
            'recommand_code',
            'clause_agree',
            'marketing_agree',
            'push_agree',
            'age',
        ]
        read_only_fields = ['pk']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    # def validate_email(self):
    #     email = self.validated_data['email']
    #     try:
    #         if KIUser.objects.filter(email=email).exists():
    #             raise serializers.ValidationError({'email': 'Email already exist'})
    #     except:
    #         return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise PasswordNotMatchingException
        data['password'] = data['password1']
        return data

    def save(self):

        email = self.validated_data['email']
        if KIUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exist'})
        username = self.validated_data['username']
        if KIUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exist'})
        nickname = self.validated_data['nickname']
        if KIUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError({'nickname': 'Nickname already exist'})

        validated_data = self.validated_data
        user = KIUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            gender=validated_data['gender'],
            birth_date=validated_data['birth_date'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            login_by='email',
        )
        return user


class KIUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KIUser
        fields = '__all__'


class KIUserKoenSerializer(serializers.Serializer):
    token = serializers.CharField()
