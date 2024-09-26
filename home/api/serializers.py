from django.contrib.auth import get_user_model
from rest_framework import serializers

from category.models import Category
from home.models import WishList, Product
from producer.models import Producer


User = get_user_model()


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ("product", "user")


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ("name", "price", "category", "description", "year", "image")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "image")


class ProducerSerializer(serializers.ModelSerializer):
    # categories = serializers.HyperlinkedRelatedField(
    #     view_name="api:api_category_detail", many=True, queryset=Category.objects.all()
    # )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )

    class Meta:
        model = Producer
        fields = ("producer_name", "description", "categories", "logo")


class ProducerWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )

    class Meta:
        model = Producer
        fields = ("producer_name", "description", "categories", "products")

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        categories_data = validated_data.pop("categories")
        producer = Producer.objects.create(**validated_data)
        producer.categories.set(categories_data)

        for product_data in products_data:
            product_data['producer'] = producer
            Product.objects.create(**product_data)

        return producer


class BasketSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_title = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.CharField(max_length=255)
    total_sum = serializers.SerializerMethodField()

    def get_total_sum(self, obj):
        request = self.context.get("request")
        basket = request.session.get("basket", {})
        total_sum = 0

        for item in basket.values():
            total_sum += item['price'] * item['quantity']

        return total_sum


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user
