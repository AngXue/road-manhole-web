from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserManagementTests(APITestCase):

    def setUp(self):
        # 创建测试用户和管理员用户
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword123')
        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

    def test_register_user(self):
        """测试用户注册"""
        url = reverse('user-api')
        data = {
            'action': 'register',
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)

    def test_login(self):
        """测试用户登录"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_update_user_info_by_user(self):
        """测试普通用户更新自己的信息"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('user-api')
        update_data = {
            'action': 'update',
            'password': 'test-newpassword'
        }
        response = self.client.post(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('test-newpassword'))

    def test_delete_user_by_username(self):
        """测试根据用户名删除用户"""
        # 确保测试时使用管理员Token进行认证
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('user-api')
        data = {
            'action': 'delete',
            'username': self.user.username
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # 确认用户确实被删除了
        self.assertFalse(User.objects.filter(username=self.user.username).exists())

    def test_get_user_info(self):
        """测试获取用户信息"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('user-api')
        data = {
            'action': 'get'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('User' in response.data)

    def test_query_user(self):
        """测试查询用户"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('user-api')
        data = {
            'action': 'query',
            'username': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
