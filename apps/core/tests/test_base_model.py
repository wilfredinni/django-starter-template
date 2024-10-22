import pytest
from django.db import connection, models, transaction

from apps.core.models import BaseModel


class TestMyModel(BaseModel):
    name = models.CharField(max_length=255)
    __test__ = False

    class Meta:
        app_label = "apps.core"
        db_table = "test_my_model"


@pytest.mark.django_db()
class TestMyAbstractModel:
    model = TestMyModel

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

    def test_update(self) -> None:
        instance = self.model.objects.create(name="Test")
        instance.name = "new value"
        instance.save()
        updated_instance = self.model.objects.get(pk=instance.pk)
        assert updated_instance.name == "new value"
        assert updated_instance.updated_at > instance.created_at
