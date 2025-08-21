from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit с валидацией."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")
        duration_seconds = data.get("duration_seconds")
        periodicity = data.get("periodicity")

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
        if duration_seconds > 120:
            raise serializers.ValidationError(
                "Время выполнения не может быть больше 120 секунд."
            )
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )
        return data

    def create(self, validated_data):
        """При создании привычки автоматически ставим пользователя из контекста
        запроса."""

        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """При обновлении нельзя менять пользователя."""

        validated_data.pop("user", None)
        return super().update(instance, validated_data)
