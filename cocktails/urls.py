from django.urls import path
from . import views
from .views import (
    ConfirmationView,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    your_account,
    CheckoutView,
    remove_from_cart_summary,
    add_to_cart_summary,
    empty_cart,
    PaymentView,
    EndView,
)

urlpatterns = [
    path('',views.allcocktails, name='allcocktails'),
    path('<int:cocktail_id>/', views.detail, name='detail'),
    path('add-to-cart/<int:cocktail_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cocktail_id>/', remove_from_cart, name='remove-from-cart'),
    path('youraccount/', your_account, name='youraccount'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirmation/',ConfirmationView.as_view(), name='confirmation'),
    path('remove-from-cart-summary/<int:cocktail_id>/', remove_from_cart_summary, name='remove-from-cart-summary'),
    path('add-to-cart-summary/<int:cocktail_id>/',add_to_cart_summary, name='add-to-cart-summary'),
    path('empty-cart/<int:cocktail_id>/',empty_cart, name='empty-cart'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('pripol/',views.pripol, name='pripol'),
    path('order-summary/pripol/',views.pripol, name='pripol'),
    path('checkout/pripol/',views.pripol, name='pripol'),
    path('confirmation/pripol/',views.pripol, name='pripol'),
    path('payment/pripol/',views.pripol, name='pripol'),
    path('end/', EndView.as_view(),name='end'),
    ]