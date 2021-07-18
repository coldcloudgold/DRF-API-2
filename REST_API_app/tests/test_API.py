import json

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from REST_API_app.models import Handbook, ItemHandbook
from REST_API_app.service.serializers import HandbookSerializer, ItemHandbookSerializer
from .data_test import Data


class TestBookViewSetField(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.init_data.create_all()
        self.url_handbook = reverse("handbook-list")
        self.url_item_handbook = reverse("item_handbook-list")
        self.url_item_handbook_validator = reverse("item_handbook_validator")

    def test_handbook_default(self):
        """Получение списка справочников."""

        needed_data = HandbookSerializer(
            [handbook for handbook in Handbook.objects.all()], many=True
        ).data

        response = self.client.get(self.url_handbook)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_handbook_actual(self):
        """Получение списка справочников, актуальных на указанную дату."""

        validity_date = {"orm": "2021-07-15", "client": "2021/07/15"}
        handbook_list = list(
            Handbook.objects.filter(
                validity_date__lte=validity_date["orm"]
            ).values_list("id", "global_id")
        )
        handbook_list.append((0, handbook_list[-1][1] + 1))
        hanbook_id_list = []

        try:
            for index in range(len(handbook_list)):
                if handbook_list[index][1] != handbook_list[index + 1][1]:
                    hanbook_id_list.append(handbook_list[index][0])
        except:
            pass

        handbooks = Handbook.objects.filter(id__in=hanbook_id_list)
        needed_data = HandbookSerializer(
            [handbook for handbook in handbooks], many=True
        ).data

        response = self.client.get(
            self.url_handbook, {"validity_date": validity_date["client"]}
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_itemhandbook_default(self):
        """Получение списка элементов справочников."""

        needed_data = ItemHandbookSerializer(
            [itemhandbook for itemhandbook in ItemHandbook.objects.all()], many=True
        ).data

        response = self.client.get(
            self.url_item_handbook,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_itemhandbook_actual(self):
        """Получение элементов заданного справочника текущей версии."""

        global_id = 2
        needed_data = ItemHandbookSerializer(
            [
                itemhandbook
                for itemhandbook in Handbook.objects.filter(global_id=global_id)
                .last()
                .items.all()
            ],
            many=True,
        ).data

        response = self.client.get(self.url_item_handbook, {"global_id": global_id})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_itemhandbook_version(self):
        """Получение элементов заданного справочника указанной версии."""

        global_id = 2
        version = "0.0.1"

        needed_data = ItemHandbookSerializer(
            [
                itemhandbook
                for itemhandbook in Handbook.objects.filter(
                    global_id=global_id,
                    version=version,
                )
                .first()
                .items.all()
            ],
            many=True,
        ).data

        response = self.client.get(
            self.url_item_handbook, {"global_id": global_id, "version": version}
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_validate_itemhanbooks_actual(self):
        """Валидация элементов заданного справочника текущей версии."""

        data = [
            {"global_id": 2},
            {"code": "Test item 1", "value": "1"},
            {"code": "Test item 2", "value": "2"},
        ]

        # "handbook": 2 <=> Справочник 2 v 0.0.2 (pk=2)
        needed_data = [
            {"id": 9, "handbook": 2, "code": "Test item 1", "value": "1"},
            {"id": 10, "handbook": 2, "code": "Test item 2", "value": "2"},
        ]

        json_data = json.dumps(data)

        response = self.client.post(
            self.url_item_handbook_validator,
            data=json_data,
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_201_CREATED, response.data["status_code"])
        self.assertEqual(needed_data, response.data["results"])

    def test_validate_itemhanbook_version(self):
        """Валидация элемента заданного справочника по указанной версии."""

        data = [
            {"global_id": 2, "version": "0.0.1"},
            {"code": "Test item 1", "value": "1"},
        ]

        # "handbook": 1 <=> Справочник 1 v 0.0.1 (pk=1)
        needed_data = [{"id": 9, "handbook": 1, "code": "Test item 1", "value": "1"}]

        json_data = json.dumps(data)

        response = self.client.post(
            self.url_item_handbook_validator,
            data=json_data,
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_201_CREATED, response.data["status_code"])
        self.assertEqual(needed_data, response.data["results"])

    def tearDown(self):
        self.init_data.delete_all()
