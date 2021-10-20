from django.contrib import admin
from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
   path('register',views.RegisterAPI.as_view(),name="register"),
   path('login',views.LoginAPI.as_view(),name="login"),
    path('email-verify',views.EmailVerify.as_view(),name="email-verify"),
   #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
   path('',views.Catalogue.as_view(),name="Catalogue"),
   path('product-create/', views.ProductCreate.as_view(), name='product-create'),
   path('product-details/<str:pk>', views.ProductRUD.as_view(), name='product-details'),
]