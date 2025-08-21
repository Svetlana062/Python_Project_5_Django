from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

User = settings.AUTH_USER_MODEL


class Habit(models.Model):
    """Модель привычки, связанная с пользователем."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
        limit_choices_to={"is_pleasant": True},
        help_text="Можно выбрать только приятную привычку",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Минимум 1, максимум 7 дней",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем вознаградить себя после выполнения",
    )
    duration_seconds = models.PositiveIntegerField(
        verbose_name="Время на выполнение (секунды)",
        help_text="Не более 120 секунд",
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        # Исключить одновременный выбор связанной привычки и вознаграждения
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать и вознаграждение, и связанную привычку."
            )

        # Время выполнения не больше 120 секунд
        if self.duration_seconds > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # Периодичность не меньше 1 и не больше 7 дней
        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

        # Если связанная привычка указана, она должна быть приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.action} at {self.time} in {self.place} ({"Pleasant" if self.is_pleasant else "Useful"})'
