import pytest

from theinkspot.category.models import Category

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list_categories(self, auth_client, user, sports_category, cs_category):
        request = auth_client.get("/api/category/")
        assert request.status_code == 200
        assert len(request.data) == 2
        assert request.data[0]["name"] == "sports"
        assert request.data[1]["name"] == "computer science"

    def test_retrive_category(self, auth_client, user, sports_category, cs_category):
        category_obj = Category.objects.get(name="sports")
        request = auth_client.get(f"/api/category/{category_obj.name}/")
        assert request.status_code == 200
        assert request.data["id"] == category_obj.id
        assert request.data["name"] == "sports"

    def test_list_categories_fail_if_not_authenticated(
        self, client, user, sports_category, cs_category
    ):
        request = client.get("/api/category/")
        assert request.status_code == 401

    def test_retrive_category_fail_if_not_authenticated(
        self, client, user, sports_category, cs_category
    ):
        id = Category.objects.get(name="sports").id
        request = client.get(f"/api/category/{id}/")
        assert request.status_code == 401
