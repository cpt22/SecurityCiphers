from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vigenere/', views.vigenere, name='vigenere'),
    path('des/', views.des, name='des'),
    path('rsa/', views.rsa, name='rsa'),
    path('md5/', views.md5, name='md5'),
    path('ci/', views.ci, name='ci'),
]