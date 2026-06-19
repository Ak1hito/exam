from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField("Название", max_length=150)
    category = models.CharField("Категория", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    sku = models.CharField("Артикул", max_length=50, unique=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def clean(self):
        errors = {}
        if not self.name.strip():
            errors["name"] = "Название товара не может быть пустым."
        if self.price is not None and self.price <= 0:
            errors["price"] = "Цена должна быть больше 0."
        if errors:
            raise ValidationError(errors)

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
