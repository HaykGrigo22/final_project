from rest_framework import serializers

from home.models import WishList


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ("product", "user")
