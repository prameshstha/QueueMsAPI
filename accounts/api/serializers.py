from rest_framework import serializers

from accounts.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name']
        # fields = [ 'email', 'password', 'password2'] just to test form flutter
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        # password2 = self.validated_data['password2']

        # if password != password2:
        #     raise serializers.ValidationError({'error': 'Both password must be same'})
        # print('pass')
        # if User.objects.filter(email=self.validated_data['email']).exists():
        #     raise serializers.ValidationError({'error': 'Email already exists!'})
        # print('email')

        account = CustomUser(email=self.validated_data['email'], first_name=self.validated_data['first_name'],
                             last_name=self.validated_data['last_name'])

        # account = User(email=self.validated_data['email'],
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'user_phone', 'is_staff', 'is_active', 'is_superuser', 'is_doc']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
