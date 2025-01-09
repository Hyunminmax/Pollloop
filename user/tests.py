from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import CustomUser


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_profile(self):
        url = '/api/user/profile/'  # 실제 URL 경로에 맞게 수정해야 합니다
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test User',
            'age': 25
        }
        response = self.client.post(url, data, format='json')

        # 테스트 실패: 예상된 상태 코드는 201이었지만, 실제로는 401을 받았습니다
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 아래는 테스트가 통과했을 경우 추가할 수 있는 assertion들입니다
        # self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())
        # user = CustomUser.objects.get(email='test@example.com')
        # self.assertEqual(user.name, 'Test User')
        # self.assertEqual(user.age, 25)
