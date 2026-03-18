
from django.urls import path

from restaurant_management.views import AddToCart, CartDeleteView, CartView, HomePageView, ProductListFetchView
app_name = "restaurant_management"
urlpatterns = [
    path("home/<str:table_id>/",HomePageView.as_view(),name="home_page"),
    path("foods/",ProductListFetchView.as_view(),name="foods"),
    path("cart/<str:table_id>/",CartView.as_view(),name="cart"),
    path("cart/delete/<str:table_id>/<int:cart_id>/",CartDeleteView.as_view(),name="cart_delete"),
    path("cart/add/<str:table_id>/",AddToCart.as_view(),name="cart_add")

]
