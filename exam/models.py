from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Product(models.Model):
    # === ТВОИ ПОЛЯ (не тронуто) ===
    name = models.CharField("Название", max_length=150)
    category = models.CharField("Категория", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    sku = models.CharField("Артикул", max_length=50, unique=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    # ===== ТЕКСТОВЫЕ ПОЛЯ =====
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Категория"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    email = models.EmailField(
        blank=True,
        unique=True,
        verbose_name="Email"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон"
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Артикул"
    )

    # ===== ЧИСЛА =====
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Цена"
    )

    views = models.IntegerField(
        default=0,
        verbose_name="Просмотры"
    )

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество"
    )

    max_guests = models.PositiveIntegerField(
        default=1,
        verbose_name="Максимум гостей"
    )

    rating = models.FloatField(
        default=0,
        verbose_name="Рейтинг"
    )

    # ===== ДАТЫ =====
    published_at = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата публикации"
    )

    event_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата мероприятия"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    # ===== BOOLEAN =====
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    # === МЕТОД clean ===
    def clean(self):
        errors = {}
        if not self.title:
            errors["title"] = "Заголовок не может быть пустым."
        if not self.name:
            errors["name"] = "Название не может быть пустым."
        if self.price <= 0:
            errors["price"] = "Цена должна быть больше 0."
        if self.views < 0:
            errors["views"] = "Просмотры не могут быть отрицательными."
        if self.max_guests <= 0:
            errors["max_guests"] = "Количество гостей должно быть больше 0."
        if self.rating < 0 or self.rating > 5:
            errors["rating"] = "Рейтинг должен быть от 0 до 5."
        if self.published_at and self.published_at > timezone.now().date():
            errors["published_at"] = "Дата публикации не может быть в будущем."
        if self.event_date and self.event_date <= timezone.now():
            errors["event_date"] = "Дата мероприятия должна быть в будущем."
        if errors:
            raise ValidationError(errors)

    # === ТВОЙ __str__ (без изменений) ===
    def __str__(self):
        return f"{self.name} ({self.sku})"

class Event(models.Model):
    title = models.CharField("Название", max_length=200)
    location = models.CharField("Место проведения", max_length=150)
    event_date = models.DateTimeField("Дата и время проведения")
    max_guests = models.PositiveIntegerField("Максимум гостей")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["event_date"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def clean(self):
        errors = {}
        if not self.title.strip():
            errors["title"] = "Название мероприятия не может быть пустым."
        if self.event_date and self.event_date <= timezone.now():
            errors["event_date"] = "Дата мероприятия должна быть в будущем."
        if self.max_guests is not None and self.max_guests <= 0:
            errors["max_guests"] = "Количество гостей должно быть больше 0."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title