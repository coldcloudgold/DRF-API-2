from rest_framework import serializers

from REST_API_app.models import Handbook, ItemHandbook


class HandbookSerializer(serializers.ModelSerializer):
    """Класс для серилизации модели "Handbook"."""

    class Meta:
        model = Handbook
        fields = "__all__"


class HandbookInItemHandbookSerializer(serializers.ModelSerializer):
    """Класс для серилизации поля handbook модели "ItemHandbook".

    Заменяет стандартный атрибут handbook ("ItemHandbook") на атрибуты "Handbook":
    - id; 
    - global_id; 
    - name;
    - version."""

    class Meta:
        model = Handbook
        fields = ("id", "global_id", "name", "version")


class ItemHandbookSerializer(serializers.ModelSerializer):
    """Класс для серилизации модели "ItemHandbook".

    Переопределен атрибут handbook"""

    handbook = HandbookInItemHandbookSerializer(read_only=True, required=False)

    class Meta:
        model = ItemHandbook
        fields = "__all__"


class ItemHandbookValidatorSerializer(serializers.ModelSerializer):
    """Класс для серилизации модели "ItemHandbook"."""

    class Meta:
        model = ItemHandbook
        fields = "__all__"
