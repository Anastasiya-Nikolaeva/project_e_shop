from django.conf import settings
from django.db import models

import users


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(
        upload_to="products/", verbose_name="Фотография", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
        ]
