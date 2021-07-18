from django.core.exceptions import ValidationError

import REST_API_app.models


class HandbookLogic:
    """Класс переопределяет стандартные функции "clean", "save".

    Добавляет проверку уникальности поля global_id в пределах одного справочника."""

    def clean(self):
        if (
            REST_API_app.models.Handbook.objects.filter(
                global_id=self.global_id, version=self.version
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError("Данная версия уже существует")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
