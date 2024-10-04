import datetime

import jwt
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from category.models import Category
from home.api.serializers import WishListSerializer, ProductSerializer, CategorySerializer, ProducerSerializer, \
    UserProfileSerializer, ProducerWithProductsSerializer

from home.models import WishList, Product
from main import settings
from producer.models import Producer


User = get_user_model()


class WishListAPIView(generics.ListAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WishList.objects.filter(user=user)


class HomeListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []


class ProducerListAPIView(generics.ListAPIView):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()
    permission_classes = []


class ProducerDetailAPIView(RetrieveAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = []


class AboutUsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        response_data = {'received_text': "About us some text"}

        return Response(response_data, status=status.HTTP_200_OK)


class BasketAddAPIView(APIView):
    permission_classes = []

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        basket = request.session.get('basket', {})

        if str(product_id) in basket:
            basket[str(product_id)]["quantity"] += 1
        else:
            basket[str(product_id)] = {
                "id": product.id,
                "product_title": product.name,
                "quantity": 1,
                "price": float(product.price),
                "image": product.image.url
            }

        request.session['basket'] = basket
        request.session.modified = True

        return Response({
            'message': f'Product {product.name} added to basket.',
            'basket': basket
        }, status=status.HTTP_200_OK)


class UserBasketAPIView(APIView):
    permission_classes = []

    def get(self, request):
        basket = request.session.get('basket', {})
        basket_items = list(basket.values())

        return Response({'basket': basket_items}, status=status.HTTP_200_OK)


class BasketDeleteAPIView(APIView):
    permission_classes = []

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        basket = request.session.get("basket", {})
        if str(product_id) in basket:
            del basket[str(product_id)]
            request.session["basket"] = basket

        return Response({
            'message': f'Product {product.name} deleted from basket.',
            'basket': basket
        }, status=status.HTTP_200_OK)


class UserProfileGetUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        data = {
            "user": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.is_active
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListItemDeleteAPIView(APIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['delete']

    def get_object(self, product_id):
        user = self.request.user
        return WishList.objects.filter(user=user, product__id=product_id)

    def delete(self, request, *args, **kwargs):
        self.get_object(kwargs.get("product_id")).delete()
        return Response({"msg": "Successfully deleted!!!"},
                        status=status.HTTP_204_NO_CONTENT)


class WishListItemADdAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)

        if WishList.objects.filter(user=request.user, product=product).exists():
            return Response(
                {"message": "Product is already in your wishlist."},
                status=status.HTTP_200_OK
            )

        WishList.objects.create(user=request.user, product=product)

        return Response(
            {"message": "Product added to your wishlist successfully."},
            status=status.HTTP_201_CREATED
        )


class ProductUpdateDeleteGetAPIView(APIView):

    def get_object(self, pk):
        airport = get_object_or_404(Product, pk=pk)
        return airport

    def put(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data,
                                       instance=self.get_object(kwargs.get("pk")))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.get_object(kwargs.get("pk")).delete()
        return Response({"msg": "Deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class SearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Adjust as needed

    def get(self, request, *args, **kwargs):
        query = request.GET.get('search')
        results = {
            "producers": [],
            "products": []
        }

        if query:
            producers = Producer.objects.filter(producer_name__icontains=query)
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

            results['producers'] = ProducerSerializer(producers, many=True).data
            results['products'] = ProductSerializer(products, many=True).data

        return Response(results)


class CategoryProducerAPIView(APIView):
    permission_classes = []

    def get(self, request, producer_id, category_id):
        products = Product.objects.filter(category__id=category_id, producer__id=producer_id)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class BasketQuantityArrowUpAPIView(APIView):
    def post(self, request, product_id):
        basket = request.session.get("basket", {})

        if str(product_id) in basket:
            basket[str(product_id)]["quantity"] += 1

        else:
            raise Http404("Product not found in the basket")

        request.session["basket"] = basket

        return Response({"success": True, "quantity": basket[str(product_id)]["quantity"]}, status=status.HTTP_200_OK)


class BasketQuantityArrowDownAPIView(APIView):
    def post(self, request, product_id):
        basket = request.session.get("basket", {})

        if str(product_id) in basket:
            if basket[str(product_id)]["quantity"] > 1:
                basket[str(product_id)]["quantity"] -= 1
            else:
                return Response({"error": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404("Product not found in the basket")

        request.session["basket"] = basket

        return Response({"success": True, "quantity": basket[str(product_id)]["quantity"]}, status=status.HTTP_200_OK)


class AdvancedSearchAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        name = request.GET.get("name")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        producer = request.GET.get("producer")
        category = request.GET.get("category")
        description = request.GET.get("description")

        all_products = Product.objects.all()
        search_list = []

        if name:
            search_list.append(Q(name__icontains=name))
        if producer:
            search_list.append(Q(producer__id=producer))
        if min_price:
            search_list.append(Q(price__gte=min_price))
        if max_price:
            search_list.append(Q(price__lte=max_price))
        if description:
            search_list.append(Q(description__icontains=description))
        if category:
            search_list.append(Q(category__id=category))

        if search_list:
            all_products = all_products.filter(*search_list)

        serialized_products = ProductSerializer(all_products, many=True)

        return Response(serialized_products.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response


class ProducerCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'producer_form': ProducerWithProductsSerializer().data
        })

    def post(self, request, *args, **kwargs):
        serializer = ProducerWithProductsSerializer(data=request.data)

        if serializer.is_valid():
            producer = serializer.save()
            return Response({
                'msg': 'Producer and Products created successfully!',
                'producer': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
