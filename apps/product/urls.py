from django.urls import path
from .views import (checkout,ListItem,ItemDetailView,
    add_to_cart,remove_from_card,OrderSummaryView,
    remove_single_item_from_card,add_single_item_to_cart,
    remove_from_card_in,remove_from_card_in)

urlpatterns = [
    path("", ListItem.as_view(),name="item_list"),
    path("checkout/", checkout, name = "checkout"),
    path("order-summary/", OrderSummaryView.as_view(), name = "order-summary"),
    path("product/<slug>/", ItemDetailView.as_view(), name = "product"),
    path("add-to-cart/<slug>/", add_to_cart, name = "addtocart"),
    path("remove-from-cart/<slug>/", remove_from_card, name = "removefromcart"),
    path("add-single-item/<slug>/", add_single_item_to_cart, name="addsingleitem"),
    path("remove-single-item/<slug>/", remove_single_item_from_card, name="removesingleitem"),
    path("remove-from-cart-all/<slug>/", remove_from_card_in, name="removefromcartall"),
]