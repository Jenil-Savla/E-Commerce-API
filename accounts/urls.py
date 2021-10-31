from django.urls import path,include
from . import views

urlpatterns = [
   path('register/',views.RegisterAPI.as_view(),name="register"),
   path('login/',views.LoginAPI.as_view(),name="login"),
   path('email-verify/',views.EmailVerify.as_view(),name="email-verify"),
   path('o-auth/',views.OAuth.as_view(),name="o-auth"),
    ]

    #Installing collected packages: pyasn1, six, rsa, pyasn1-modules, protobuf, cachetools, httplib2, googleapis-common-protos, google-auth, google-auth-httplib2, google-api-core, google-api-python-client
