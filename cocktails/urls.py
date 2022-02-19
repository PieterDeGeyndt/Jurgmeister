from django.urls import path
from . import views
from .views import add_to_cart,remove_from_cart,your_cart,your_account

urlpatterns = [
    path('',views.allcocktails, name='allcocktails'),
    path('<int:cocktail_id>/', views.detail, name='detail'),
    path('add-to-cart/<int:cocktail_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cocktail_id>/', remove_from_cart, name='remove-from-cart'),
    path('youraccount/', your_account, name='youraccount'),
    path('yourcart/', your_cart, name='yourcart'),
    ]