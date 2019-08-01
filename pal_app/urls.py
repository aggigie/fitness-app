from django.urls import path

from pal_app import views

urlpatterns = [
    path('add-product/', views.add_product),
    path('products/', views.show_products),
    path('', views.main),
    path('user-data/', views.user_data),
    path('meal/<int:meal_type>/', views.meal_data)
]
