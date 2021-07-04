from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Diary


class LoggedInTestCase(TestCase):
    """ 各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        self.password = "TestUser1234"

        self.test_user = get_user_model().objects.create_user(
            username="TestUser",
            email="testuser@example.com",
            password=self.password
        )

        self.client.login(
            email=self.test_user.email,
            password=self.password
        )


class TestDiaryCreateView(LoggedInTestCase):
    """DiaryCreateView用のテストクラス"""

    def test_create_diary_success(self):
        params = {
            "title": "test title",
            "content": "test contents",
            "photo1": "",
            "photo2": "",
            "photo3": ""
        }
        response = self.client.post(reverse_lazy("diary:diary_create"), params)

        self.assertRedirects(response, reverse_lazy("diary: diary_list"))
        self.assertEqual(Diary.objects.filter(title="test title").count(), 1)

    def test_create_diary_failure(self):
        response = self.client.post(reverse_lazy("diary: diary_create"))
        self.assertFormError(response, "form", "title", "このフィールドは必須です。")


class TestDiaryUpdateViwe(LoggedInTestCase):
    """DiaryUpdateView用のテストクラス"""

    def test_update_diary_success(self):
        diary = Diary.objects.create(user=self.test_user, title="タイトル編集前")
        params = {"title": "タイトル編集後"}
        response = self.client.post(reverse_lazy("diary: diary_ipdate", kwargs={"pk": diary.pk}), params)
        self.assertRedirects(response, reverse_lazy("diary: diary_detail", kwargs={"pk": diary.pk}))