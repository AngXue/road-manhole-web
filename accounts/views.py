from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from .models import UserProfile

from visualize_data.ultralyticsapi.UseAndSave import model_run, save_results


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
        # 从请求中获取要更新的用户名和密码
        username_to_update = request.data.get('username')
        new_password = request.data.get('password')

        # 确定目标用户，默认为当前认证用户
        if request.user.is_staff and username_to_update:
            # 如果操作用户是管理员且指定了用户名，尝试获取该用户
            try:
                target_user = User.objects.get(username=username_to_update)
            except User.DoesNotExist:
                return Response({"detail": "指定的用户不存在。"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 普通用户只能更新自己的密码
            target_user = request.user
            if username_to_update and username_to_update != request.user.username:
                return Response({"detail": "没有权限更新其他用户的信息。"}, status=status.HTTP_403_FORBIDDEN)

        # 更新密码
        if new_password:
            target_user.set_password(new_password)
            target_user.save()
            return Response({"message": "密码更新成功。"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "未提供新密码。"}, status=status.HTTP_400_BAD_REQUEST)

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


class UseModelAPIView(APIView):
    def get_all_models(self, request):
        """
        获取所有模型
        :param request:
        :return:
        """
        # 调用clearml的接口获取所有模型
        # TODO: 未实现
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "未认证的用户。"}, status=status.HTTP_401_UNAUTHORIZED)

        return []

    def predict_data(self, request):
        """
        预测数据
        :param request:
        :return: 预测结果
        """
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "未认证的用户。"}, status=status.HTTP_401_UNAUTHORIZED)

        data_path = request.data.get('data_path')
        model_path = request.data.get('model_path')

        results = model_run(model_path, data_path)

        result_dir = 'data_path/test_results'
        if os.path.exists(result_dir):
            # 删除文件夹及其内容
            shutil.rmtree(result_dir)
        os.mkdir(result_dir)

        # 保存所有对象检测结果至一个文件
        results_txt = 'data_path/results.txt'
        if os.path.exists(results_txt):
            os.remove(results_txt)

        # [{filename, cls_list}, ...]
        return save_results(results, results_txt, result_dir)
