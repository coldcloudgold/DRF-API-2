from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView

from .models import Handbook, ItemHandbook

from .service.serializers import HandbookSerializer, ItemHandbookSerializer
from .service.businnes_views import (
    HandbookViewSetLogic,
    ItemHandbookViewSetLogic,
    ItemHandbookValidatorLogic,
)


class HandbookViewSet(HandbookViewSetLogic, ReadOnlyModelViewSet):
    """Класс предоставляет возможности:
    - Получение списка справочников;
    - Получение списка справочников, актуальных на указанную дату."""

    model = Handbook
    serializer_class = HandbookSerializer


class ItemHandbookViewSet(ItemHandbookViewSetLogic, ReadOnlyModelViewSet):
    """Класс предоставляет возможности:
    - Получение элементов заданного справочника указанной версии;
    - Получение элементов заданного справочника текущей версии;
    - Получение всех элементов справочников."""

    model = ItemHandbook
    serializer_class = ItemHandbookSerializer


class ItemHandbookValidator(ItemHandbookValidatorLogic, APIView):
    """Класс определяет метод POST.

    Возможности:
    - Валидация элементов заданного справочника текущей версии;
    - Валидация элемента заданного справочника по указанной версии."""

    pass
