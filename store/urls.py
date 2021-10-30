from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products',views.ProductViewSet, basename = 'product')
urlpatterns = [
   #path('',views.Catalogue.as_view(),name="Catalogue"),
   path('product-create/', views.ProductCreate.as_view(), name='product-create'),
   path('product-details/<str:pk>', views.ProductDetails.as_view(), name='product-details'),
]

urlpatterns += router.urls