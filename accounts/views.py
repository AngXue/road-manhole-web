from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserAPI(APIView):
    # 设置为任何人都可以访问注册接口
    permission_classes_by_action = {
        'register': (permissions.AllowAny,),
        'login': (permissions.AllowAny,),
        'logout': (permissions.IsAuthenticated,),
    }

    def get_permissions(self):
        # 检查self是否有action属性，如果没有，则设置为None
        action = getattr(self, 'action', None)

        # 现在使用action变量来获取权限类列表
        if action and action in self.permission_classes_by_action:
            # 返回适用于当前 action 的权限类列表
            return [permission() for permission in self.permission_classes_by_action[action]]
        else:
            # 如果当前 action 没有特定的权限设置，则返回默认权限设置
            return [permission() for permission in self.permission_classes]

    def post(self, request, action):
        self.action = action
        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        elif action == 'logout':
            return self.logout(request)
        else:
            return Response({"error": "Not a valid action"}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
