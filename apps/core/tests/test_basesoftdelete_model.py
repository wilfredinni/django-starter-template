import pytest
from django.db import connection, models, transaction

from apps.core.models import SoftDeleteBaseModel


class TestSoftDeleteModel(SoftDeleteBaseModel):
    name = models.CharField(max_length=255)
    __test__ = False

    class Meta:
        app_label = "apps.core"
        db_table = "test_soft_delete_model"


@pytest.mark.django_db()
class TestSoftDeleteBaseModel:
    model = TestSoftDeleteModel

    def setup_method(self, method):
        with transaction.atomic():
            with connection.schema_editor() as schema_editor:
                schema_editor.connection.in_atomic_block = False
                schema_editor.create_model(self.model)
                schema_editor.connection.in_atomic_block = True

    def teardown_method(self, method):
        with transaction.atomic():
            with connection.schema_editor() as schema_editor:
                schema_editor.connection.in_atomic_block = False
                schema_editor.delete_model(self.model)
                schema_editor.connection.in_atomic_block = True

    def test_create(self) -> None:
        instance = self.model.objects.create(name="Test")
        assert instance.pk is not None
        assert instance.name == "Test"
        assert instance.created_at is not None
        assert instance.updated_at is not None
        assert instance.deleted_at is None

    def test_soft_delete(self) -> None:
        instance = self.model.objects.create(name="Test")
        instance.delete()
        assert instance.deleted_at is not None
        assert instance.updated_at is not None
        assert instance.created_at is not None
        assert instance.updated_at > instance.created_at
        assert self.model.objects.filter(pk=instance.pk).exists() is False

    def test_queryset_soft_delete(self) -> None:
        instance = self.model.objects.create(name="Test")
        instance1 = self.model.objects.create(name="Test2")
        assert self.model.objects.count() == 2

        self.model.objects.all().delete()

        assert self.model.objects.filter(pk=instance.pk).exists() is False
        assert self.model.objects.filter(pk=instance1.pk).exists() is False
        assert self.model.objects.count() == 0
