from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit


User = get_user_model()


class HabitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            "action": "Читать книгу",
            "time": "08:00:00",
            "place": "Дом",
            "periodicity": 3,
            "duration_seconds": 60,
            "is_pleasant": False,
            "reward": "Шоколад",
            "is_public": True,
        }
        # Исправлено: URL теперь /api/habits/
        response = self.client.post("/api/habits/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.action, "Читать книгу")

    def test_validation_reward_and_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            action="Медитация",
            time="07:00:00",
            place="Парк",
            periodicity=1,
            duration_seconds=30,
            is_pleasant=True,
            is_public=False,
        )
        data = {
            "action": "Спорт",
            "time": "18:00:00",
            "place": "Зал",
            "periodicity": 2,
            "duration_seconds": 90,
            "is_pleasant": False,
            "reward": "Пицца",
            "related_habit": pleasant_habit.id,
            "is_public": False,
        }
        # Исправлено: URL теперь /api/habits/
        response = self.client.post("/api/habits/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя одновременно указывать", str(response.data))
