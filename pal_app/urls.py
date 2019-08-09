from django.urls import path

from pal_app import views

urlpatterns = [
    path('add-product/', views.add_product),
    path('products/', views.show_products),
    path('', views.main),
    path('user-data/', views.user_data),
    path('delete-account/', views.delete_user, name="delete_user"),
    path('remove-product/<int:product_id>/', views.remove_product, name="remove_product"),
    path('meal/<int:meal_type>/', views.meal_data)
]
