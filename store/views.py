from .models import Product,Category
from .serializers import ProductSerializer

from rest_framework.generics import GenericAPIView
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .permissions import SellerStatus


class Catalogue(mixins.ListModelMixin,GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    
    queryset = Product.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

        
class ProductCreate(SellerStatus,mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ProductSerializer
    permission_classes = [SellerStatus,IsAuthenticated,]
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        cat = request.data['category']
        id = cat.get('id')
        category = Category.objects.get(id = id)
        return self.create(request, *args, **kwargs)

class ProductDetails(SellerStatus,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = ProductSerializer
    permission_classes = [SellerStatus,IsAuthenticated,]
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.destroy(request, *args, **kwargs)
