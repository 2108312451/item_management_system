from django.urls import path, include
from AllUser.views import Login

urlpatterns = [
    path('ordinaryuserlogin/',Login.OrdinaryUserLoginView.as_view(),name='ordinaryuserlogin'),
    path('codelogin/',Login.CodesView.as_view(),name='codelogin'),
    path('regular_administratorlogin/',Login.Regular_AdministratorLoginView.as_view(),name='regular_administratorlogin'),
    path('super_administratorlogin/',Login.Super_AdministratorLoginView.as_view(),name='super_administratorlogin'),
]