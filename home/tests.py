from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from category.models import Category
from home.models import WishList, Product
from producer.models import Producer

User = get_user_model()


class WishListApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(email="test_email@yopmail.com", password="testpassword")
        self.test_user2 = User.objects.create_user(email="test2_email@yopmail.com", password="testpassword")

        product1 = Product.objects.create(name="test_product1", price=111, year=2011, description="test desc1")
        product2 = Product.objects.create(name="test_product2", price=222, year=2022, description="test desc2")

        self.wish_list_object1 = WishList.objects.create(user=self.test_user, product=product1)
        self.wish_list_object2 = WishList.objects.create(user=self.test_user, product=product2)

        self.url = reverse("api:wish_list_api")

    def get_jwt_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_authenticated_user_can_access_wishlist(self):
        token = self.get_jwt_token_for_user(self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        print(response.data)
        self.assertEqual(response.data[0]["product"], 2)
        self.assertEqual(response.data[0]["user"], 1)
        self.assertEqual(response.data[1]["product"], 3)
        self.assertEqual(response.data[1]["user"], 1)

    def test_unauthenticated_user_cannot_access_wishlist(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_empty_wish_list(self):
        token = self.get_jwt_token_for_user(self.test_user2)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 0)


class AddProductViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Producer", description="Test desc cat")
        self.producer = Producer.objects.create(producer_name="Test Category", description="Test desc prod")

        self.producer.categories.set([self.category])

        self.url = reverse("home:add_product")

    def test_add_product_view(self):
        data = {
            "name": "Test Product",
            "price": 100,
            "producer": self.producer.id,
            "category": self.category.id,
            "description": "Test description",
            "year": 2022,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertTrue(Product.objects.filter(name="Test Product").exists())

        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.producer, self.producer)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.year, 2022)
        self.assertEqual(product.description, "Test description")
