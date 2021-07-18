from REST_API_app.models import Handbook, ItemHandbook


class Data:
    """Класс для быстрого созданния данных для тестов."""

    def create_hanbook(self):
        self.handbook_1 = Handbook.objects.create(
            global_id=1,
            name="Справочник 1 v 0.0.1",
            short_name="1 v 0.0.1",
            description="Информация",
            version="0.0.1",
            validity_date="2021-07-15",
        )

        return self.handbook_1

    def create_handbooks(self):
        self.handbook_2 = Handbook.objects.create(
            global_id=2,
            name="Справочник 2 v 0.0.1",
            short_name="2 v 0.0.1",
            description="Информация",
            version="0.0.1",
            validity_date="2021-07-15",
        )
        self.handbook_3 = Handbook.objects.create(
            global_id=2,
            name="Справочник 2 v 0.0.2",
            short_name="2 v 0.0.2",
            description="Информация",
            version="0.0.2",
            validity_date="2021-07-15",
        )
        self.handbook_4 = Handbook.objects.create(
            global_id=3,
            name="Справочник 3 v 0.0.1",
            short_name="3 v 0.0.1",
            description="Информация",
            version="0.0.1",
            validity_date="2021-07-15",
        )
        self.handbook_5 = Handbook.objects.create(
            global_id=3,
            name="Справочник 3 v 0.0.2",
            short_name="3 v 0.0.2",
            description="Информация",
            version="0.0.2",
            validity_date="2021-07-15",
        )

        return self.handbook_5

    def delete_handbooks(self):
        Handbook.objects.all().delete()

    def create_itemhanbook(self):
        self.itemhanbook_1 = ItemHandbook.objects.create(
            handbook=self.handbook_1, code="1", value="1"
        )

        return self.itemhanbook_1

    def create_itemhanbooks(self):
        self.itemhanbook_2 = ItemHandbook.objects.create(
            handbook=self.handbook_2, code="1", value="1"
        )
        self.itemhanbook_3 = ItemHandbook.objects.create(
            handbook=self.handbook_2, code="2", value="2"
        )
        self.itemhanbook_4 = ItemHandbook.objects.create(
            handbook=self.handbook_3, code="1", value="1"
        )
        self.itemhanbook_5 = ItemHandbook.objects.create(
            handbook=self.handbook_3, code="2", value="2"
        )
        self.itemhanbook_5 = ItemHandbook.objects.create(
            handbook=self.handbook_4, code="1", value="1"
        )
        self.itemhanbook_6 = ItemHandbook.objects.create(
            handbook=self.handbook_4, code="2", value="2"
        )
        self.itemhanbook_7 = ItemHandbook.objects.create(
            handbook=self.handbook_5, code="1", value="1"
        )
        self.itemhanbook_8 = ItemHandbook.objects.create(
            handbook=self.handbook_5, code="2", value="2"
        )

        return self.itemhanbook_8

    def delete_itemhandbooks(self):
        ItemHandbook.objects.all().delete()

    def create_all(self):
        handbook = self.create_handbooks()
        itemhandbook = self.create_itemhanbooks()

        return [handbook, itemhandbook]

    def delete_all(self):
        self.delete_itemhandbooks()
        self.delete_handbooks()
