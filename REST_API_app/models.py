from datetime import date

from django.db import models

from .service.businnes_models import HandbookLogic


class Handbook(HandbookLogic, models.Model):
    """Модель "Справочник".

    Атрибуты:
    Идентификатор справочника
    Наименование
    Короткое наименование
    Описание
    Версия (уникальная в пределах одного справочника)
    Дата начала действия справочника
    """

    global_id = models.PositiveIntegerField(
        default=1, verbose_name="Глобальный идентификатор"
    )
    name = models.CharField(max_length=255, verbose_name="Наименование")
    short_name = models.CharField(max_length=140, verbose_name="Короткое наименование")
    description = models.TextField(verbose_name="Описание")
    version = models.CharField(max_length=155, verbose_name="Версия")
    validity_date = models.DateField(
        default=date.today, verbose_name="Начало действия"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class ItemHandbook(models.Model):
    """Модель "Элемент справочника".

    Атрибуты:
    Идентификатор
    Родительский идентификатор
    Код элемента
    Значение элемента
    """

    handbook = models.ForeignKey(
        Handbook,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Справочник",
    )
    code = models.CharField(max_length=140, verbose_name="Код")
    value = models.CharField(max_length=140, verbose_name="Значение")

    def __str__(self) -> str:
        return f"{self.handbook.name}: {self.value}"

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"
