from rest_framework import serializers

from django.contrib.auth import authenticate

from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    '''Сериализатор регистрации нового не подтвержденного пользователя'''
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Данное имя недоступно!')
        return value

    def validate(self, data):
        if data.get('email') is None:
            raise serializers.ValidationError('email is required field')
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GetTokenSerializer(serializers.Serializer):
    ''' Выдача токена, активация не активированной учетной записи'''
    confirm_code = serializers.IntegerField(write_only=True, required=False)
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid username and/or password')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        if user.is_confirm is False:
            if user.confirm_code == data.get('confirm_code'):
                user.is_confirm = True
                user.save()
                return {
                    "token": user.token
                }
            raise serializers.ValidationError('Invalid confirmation code')

        return {
            "token": user.token
        }


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    is_confirm = serializers.BooleanField(
        default=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'bio', 'role', 'is_confirm')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)
