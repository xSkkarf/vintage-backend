from rest_framework import generics, status
from rest_framework.response import Response
from store.models import Product
from store.serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            return Response({"error": "Products not found"}, status=status.HTTP_404_NOT_FOUND)

class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)