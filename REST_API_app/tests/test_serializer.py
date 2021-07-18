from REST_API_app.models import Handbook, ItemHandbook
from django.test import TestCase

from REST_API_app.service.serializers import (
    HandbookSerializer,
    HandbookInItemHandbookSerializer,
    ItemHandbookSerializer,
    ItemHandbookValidatorSerializer,
)

from .data_test import Data


class TestSerializers(TestCase):
    def setUp(self):
        self.init_data = Data()
        self.init_data.create_all()

    def test_hanbookserializer(self):
        handbooks = Handbook.objects.all()
        data = HandbookSerializer([handbook for handbook in handbooks], many=True).data
        needed_data = []

        for handbook in handbooks:
            needed_data.append(
                {
                    "id": handbook.id,
                    "global_id": handbook.global_id,
                    "name": handbook.name,
                    "short_name": handbook.short_name,
                    "description": handbook.description,
                    "version": handbook.version,
                    "validity_date": "2021-07-15",
                }
            )

        self.assertEqual(needed_data, data)

    def test_handbookinitemhandbookserializer(self):
        itemhandbooks = ItemHandbook.objects.all()
        handbooks = Handbook.objects.all()
        data = HandbookInItemHandbookSerializer(
            [handbook for handbook in handbooks], many=True
        ).data
        needed_data = []

        for handbook in handbooks:
            needed_data.append(
                {
                    "id": handbook.id,
                    "global_id": handbook.global_id,
                    "name": handbook.name,
                    "version": handbook.version,
                }
            )

        self.assertEqual(needed_data, data)

    def test_itemhandbookserializer(self):
        itemhandbooks = ItemHandbook.objects.all()
        data = ItemHandbookSerializer(
            [itemhandbook for itemhandbook in itemhandbooks], many=True
        ).data
        needed_data = []

        for itemhandbook in itemhandbooks:
            needed_data.append(
                {
                    "id": itemhandbook.id,
                    "handbook": {
                        "id": itemhandbook.handbook.id,
                        "global_id": itemhandbook.handbook.global_id,
                        "name": itemhandbook.handbook.name,
                        "version": itemhandbook.handbook.version,
                    },
                    "code": itemhandbook.code,
                    "value": itemhandbook.value,
                }
            )

        self.assertEqual(needed_data, data)

    def test_itemhandbookvalidatorserializer(self):
        itemhandbooks = ItemHandbook.objects.all()
        data = ItemHandbookValidatorSerializer(
            [itemhandbook for itemhandbook in itemhandbooks], many=True
        ).data
        needed_data = []

        for itemhandbook in itemhandbooks:
            needed_data.append(
                {
                    "id": itemhandbook.id,
                    "handbook": itemhandbook.handbook.id,
                    "code": itemhandbook.code,
                    "value": itemhandbook.value,
                }
            )

        self.assertEqual(needed_data, data)

    def tearDown(self):
        self.init_data.delete_all()
