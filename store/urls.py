from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.Catalogue.as_view(),name="Catalogue"),
   path('product-create/', views.ProductCreate.as_view(), name='product-create'),
   path('product-details/<str:pk>', views.ProductDetails.as_view(), name='product-details'),
]