from django.urls import path
from . import views

urlpatterns = [
   path('cart',views.CartView.as_view(),name="cart"),
   path('pay/<str:pk>/', views.start_payment, name="start_payment"),
    path('handlepayment/', views.handlepayment, name="handlepayment"),
   ]