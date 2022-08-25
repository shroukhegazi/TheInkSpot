import pytest
from django.db import IntegrityError

from theinkspot.category.models import Category

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCategoryModel:
    def test_unique_constriant_on_category_name(self, sports_category):
        with pytest.raises(IntegrityError):
            Category.objects.create(name="sports")

    def test_create_category(self, sports_category):
        category = Category.objects.filter(name="sports").first()
        assert Category.objects.all().count() == 1
        assert category.name == sports_category.name
