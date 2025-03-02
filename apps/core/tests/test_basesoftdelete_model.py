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

    def test_restore(self) -> None:
        instance = self.model.objects.create(name="Test")
        instance.delete()
        instance.restore()
        assert instance.deleted_at is None
        assert self.model.objects.filter(pk=instance.pk).exists()

    def test_hard_delete(self) -> None:
        instance = self.model.objects.create(name="Test")
        instance.delete(hard_delete=True)
        assert not self.model.objects.all_with_deleted().filter(id=instance.id).exists()

    def test_deleted_manager_method(self) -> None:
        """Test that deleted() manager method returns only soft-deleted objects"""
        instance1 = self.model.objects.create(name="Test1")
        instance2 = self.model.objects.create(name="Test2")
        instance3 = self.model.objects.create(name="Test3")

        # Delete two instances
        instance1.delete()
        instance2.delete()

        # Check regular queryset
        assert self.model.objects.count() == 1
        assert self.model.objects.first() == instance3

        # Check deleted queryset
        deleted_objects = self.model.objects.deleted()
        assert deleted_objects.count() == 2
        assert instance1 in deleted_objects
        assert instance2 in deleted_objects
        assert instance3 not in deleted_objects

    def test_all_with_deleted_manager_method(self) -> None:
        """Test that all_with_deleted() manager method returns all objects"""
        instance1 = self.model.objects.create(name="Test1")
        instance2 = self.model.objects.create(name="Test2")
        instance3 = self.model.objects.create(name="Test3")

        # Delete one instance
        instance2.delete()

        # Check regular queryset
        assert self.model.objects.count() == 2

        # Check all_with_deleted queryset
        all_objects = self.model.objects.all_with_deleted()
        assert all_objects.count() == 3
        assert instance1 in all_objects
        assert instance2 in all_objects
        assert instance3 in all_objects

    def test_queryset_chaining_with_deleted(self) -> None:
        """Test that manager methods can be chained with other queryset methods"""
        instance1 = self.model.objects.create(name="Test1")
        instance2 = self.model.objects.create(name="Test2")
        instance3 = self.model.objects.create(name="Test3")

        instance1.delete()
        instance2.delete()

        # Test filtering on deleted queryset
        deleted_test1 = self.model.objects.deleted().filter(name="Test1")
        assert deleted_test1.count() == 1
        assert deleted_test1.first() == instance1

        # Test ordering on all_with_deleted queryset
        all_ordered = self.model.objects.all_with_deleted().order_by("-name")
        assert list(all_ordered) == [instance3, instance2, instance1]
