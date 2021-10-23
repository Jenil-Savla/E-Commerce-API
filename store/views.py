from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer

from rest_framework.generics import GenericAPIView
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import SellerPermission

class Catalogue(mixins.ListModelMixin,GenericAPIView):
	
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

class ProductCreate(mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser,]
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)


class ProductDetails(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser,]
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
