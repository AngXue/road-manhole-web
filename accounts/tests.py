from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserAccountTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 为了简化，创建一个用户供测试使用
        cls.user_data = {'username': 'testuser', 'password': 'testpassword123', 'email': 'test@example.com'}
        cls.user = User.objects.create_user(**cls.user_data)
        cls.token, _ = Token.objects.get_or_create(user=cls.user)

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_registration(self):
        """
        测试用户注册。
        """
        url = reverse('user-api', args=['register'])
        data = {'username': 'newuser', 'password': 'newpassword123', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 确认新用户创建成功
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """
        测试用户登录。
        """
        url = reverse('user-api', args=['login'])
        data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user_info(self):
        """
        测试获取用户信息。
        """
        # 先登录获取Token
        self.test_user_login()
        token = self.client.post(reverse('api_token_auth'), self.user_data, format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # 注意使用 'user-api-with-pk'
        url = reverse('user-api-with-pk', args=['detail', self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user_info(self):
        """
        测试更新用户信息。
        """
        url = reverse('user-api-with-pk', kwargs={'action': 'update', 'pk': self.user.id})
        data = {'first_name': 'NewFirstName', 'last_name': 'NewLastName'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'NewFirstName')
        self.assertEqual(updated_user.last_name, 'NewLastName')

    def test_delete_user(self):
        """
        测试删除用户。
        """
        url = reverse('user-api-with-pk', kwargs={'action': 'delete', 'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
