import datetime

from rest_framework import status
from rest_framework.response import Response

import REST_API_app.models
import REST_API_app.service.serializers


class HandbookViewSetLogic:
    """Класс переопределяет стандартный get_queryset.

    Добавляет возможности:
    - Получение списка справочников, актуальных на указанную дату;
    - Получение списка справочников."""

    def get_queryset(self):
        validity_date = self.request.GET.get("validity_date", None)

        # преборазование validity_date к datetime, в противном случае - возрат пустого списка
        if validity_date:
            try:
                validity_date = datetime.datetime.strptime(validity_date, "%Y/%m/%d")
            except:
                return []

        # получение списка справочников, актуальных на указанную дату, в противном случае - возрат пустого списка
        if validity_date:
            try:
                # получение кортежа из id, global_id всех справочников, с ранней или равной датой
                handbook_list = list(
                    REST_API_app.models.Handbook.objects.filter(
                        validity_date__lte=validity_date
                    ).values_list("id", "global_id")
                )
                # добавление элемента, благодря которому происходит полное заполнение hanbook_id_list
                handbook_list.append((0, handbook_list[-1][1] + 1))
                hanbook_id_list = []

                try:
                    for index in range(len(handbook_list)):
                        if handbook_list[index][1] != handbook_list[index + 1][1]:
                            # добавление id справочника, если не совпадают global_id
                            hanbook_id_list.append(handbook_list[index][0])
                except:
                    pass

                return REST_API_app.models.Handbook.objects.filter(
                    id__in=hanbook_id_list
                )

            except:
                return []

        # получение списка справочников
        else:
            return REST_API_app.models.Handbook.objects.all()


class ItemHandbookViewSetLogic:
    """Класс переопределяет стандартный get_queryset.

    Добавляет возможности:
    - Получение элементов заданного справочника указанной версии;
    - Получение элементов заданного справочника текущей версии;
    - Получение всех элементов справочников."""

    def get_queryset(self):
        global_id = self.request.GET.get("global_id", None)
        version = self.request.GET.get("version", None)

        # преборазование global_id к int, в противном случае - возрат пустого списка
        if global_id:
            try:
                global_id = int(global_id)
            except:
                return []
        if version:
            version = str(version)

        # получение элементов заданного справочника указанной версии, в противном случае - возрат пустого списка
        if global_id and version:
            try:
                return (
                    REST_API_app.models.Handbook.objects.filter(
                        global_id=global_id,
                        version=version,
                    )
                    .first()
                    .items.all()
                )
            except:
                return []

        # получение элементов заданного справочника текущей версии, в противном случае - возрат пустого списка
        elif global_id:
            try:
                return (
                    REST_API_app.models.Handbook.objects.filter(global_id=global_id)
                    .last()
                    .items.all()
                )
            except:
                return []

        # получение всех элементов справочников
        else:
            return REST_API_app.models.ItemHandbook.objects.all()


class ItemHandbookValidatorLogic:
    """Класс определяет метод POST.

    Возможности:
    - Валидация элементов заданного справочника текущей версии;
    - Валидация элемента заданного справочника по указанной версии."""

    def post(self, request, format=None):
        data_global = request.data
        data_objects = []
        global_id = None
        version = None
        results = []
        status_code = status.HTTP_400_BAD_REQUEST

        # получение global_id и version из запроса, добавление элементов для будущей валидации
        for item in data_global:
            if "global_id" and "version" in item:
                global_id = item["global_id"]
                version = item["version"]
            elif "global_id" in item:
                global_id = item["global_id"]
            else:
                data_objects.append(item)

        # преборазование global_id к int, в противном случае - возрат пустого списка
        if global_id:
            try:
                global_id = int(global_id)
            except:
                return Response(
                    {
                        "method": "POST",
                        "status": status_code,
                        "results": results,
                    }
                )
        if version:
            version = str(version)

        # получение объекта Hanbook
        if global_id and version:
            handbook = REST_API_app.models.Handbook.objects.filter(
                global_id=global_id, version=version
            ).last()
        elif global_id:
            handbook = REST_API_app.models.Handbook.objects.filter(
                global_id=global_id
            ).last()

        if handbook:
            for objects in data_objects:
                # добавление id к каждому элементу Itemhanbook (handbook - foreingkey)
                objects["handbook"] = handbook.id

            # сериализация обработнных данных
            serializer = (
                REST_API_app.service.serializers.ItemHandbookValidatorSerializer(
                    data=data_objects, many=True
                )
            )

            # валидация и сохранение объектов
            if serializer.is_valid():
                if serializer.save():
                    results = serializer.data
                    status_code = status.HTTP_201_CREATED

        return Response(
            {
                "method": "POST",
                "status_code": status_code,
                "results": results,
            }
        )
