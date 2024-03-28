from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from .models import UserProfile


class UserAPIView(APIView):
    # 允许任何人访问注册接口，但登录后的操作需要认证
    def get_permissions(self):
        if self.request.method == 'POST':
            action = self.request.data.get('action')
            if action == 'register':
                return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def post(self, request):
        action = request.data.get('action')
        if action == 'register':
            return self.register(request)
        elif action == 'update':
            return self.update(request)
        elif action == 'delete':
            return self.delete(request)
        elif action == 'get':
            return self.get(request)
        elif action == 'query':
            return self.query(request)
        else:
            return Response({"error": "无效的操作"}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = UserRegisterSerializer(user).data
            return Response({"message": "用户注册成功", "user": user}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.is_staff or user.username == request.data.get('username', ''):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"detail": "没有权限更新其他用户的信息。"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user_name = request.data.get('username')
            user_to_delete = User.objects.get(username=user_name)
            if request.user.is_staff or request.user == user_to_delete:
                user_to_delete.delete()
                return Response({"message": "用户删除成功。"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "没有权限删除其他用户。"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "用户不存在。"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        # 使用request.user直接获取当前认证的用户对象
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "未认证的用户。"}, status=status.HTTP_401_UNAUTHORIZED)

        user = UserSerializer(user).data
        return Response({"User": user}, status=status.HTTP_200_OK)

    def query(self, request):
        username = request.data.get('username')
        users = User.objects.filter(username__icontains=username)
        if request.user.is_staff:
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "只有管理员可以查询用户。"}, status=status.HTTP_403_FORBIDDEN)
