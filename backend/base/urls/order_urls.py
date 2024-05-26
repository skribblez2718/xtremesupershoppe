from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('', views.get_orders, name="get-orders"),
    path('add/', views.add_order_items, name="orders-add"),
    path('myorders/', views.get_my_orders, name="myorders"),
    path('<str:pk>/delivered/', views.update_order_to_delivered, name="user-delivered"),
    path('<str:pk>/', views.get_order_by_id, name="user-order"),
    path('<str:pk>/pay/', views.update_order_to_paid, name="pay"),
]