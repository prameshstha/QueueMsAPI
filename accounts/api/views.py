from django.contrib.auth import logout, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json

from .serializers import RegistrationSerializer
from rest_framework import parsers, renderers, generics, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from accounts.models import CustomUser


class RegistrationView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            print('valid')
            user = serializer.save()
            token = Token.objects.create(user=user)
            data['email'] = user.email
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['is_active'] = user.is_active
            data['is_staff'] = user.is_staff
            data['is_superuser'] = user.is_superuser
            data['user_phone'] = user.user_phone
            data['token'] = token.key
            data['user_id'] = user.id

            return Response(data, 200)
        else:
            data = serializer.errors
            # print(data)
            # a = json.dumps(data.get('email'))
            # print(list(data))
            # if a==["CustomUser with this email already exists."]:
            #     print('sy')

        return Response(data, 403)


class Login(APIView):
    # below def get is to show the list of users but it is not required in login so it is commented.

    # def get(self, request):
    #     print(request.GET)
    #     queryset = User.objects.all()
    #     serializer = LoginSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        email = request.data['email']
        password = request.data['password']

        if email and password:
            try:
                # Try to find a user matching your username
                user = CustomUser.objects.get(email=email)
                pwd_valid = check_password(password, user.password)
                print(pwd_valid)
                #  Check the password is the reverse of the username
                # something wrong here need to check asap
                if pwd_valid:
                    # Yes? return the Django user object
                    token = Token.objects.get_or_create(user=user)
                    user_dict = (model_to_dict(user))
                    user_dict.pop('last_login')
                    user_dict.pop('date_joined')
                    user_dict.pop('groups')
                    user_dict.pop('user_permissions')
                    user_dict.pop('password')
                    print(token[0])
                    user_dict['token'] = str(token[0])
                    return Response(user_dict, 200)
                else:
                    # No? return None - triggers default login failed
                    return Response({'Error': 'Email or Password wrong'}, 403)
            except CustomUser.DoesNotExist:
                # No user was found, return None - triggers default login failed
                return Response({'Error': 'User Does not exist'}, 404)


class Logout(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        print(request.data)
        logout(request)
        return Response({'message': 'User Logged out'})


class UserListUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'


class AllUsersList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class GetAvailableDoc(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_doc=True)
    serializer_class = UserSerializer
