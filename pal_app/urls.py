from django.urls import path

from pal_app import views

urlpatterns = [
    path('addProduct/', views.add_product),
    path('products/', views.show_products),
    path('', views.main)
]
