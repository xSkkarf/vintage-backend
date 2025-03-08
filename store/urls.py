
from django.urls import path
import store.views.cartView as cartView
import store.views.orderView as orderView
import store.views.productView as productView
import store.views.shipmentView as shipmentView

urlpatterns = [
    path('products/', productView.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', productView.ProductDetailView.as_view(), name='product-detail'),

    path('cart/', cartView.CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', cartView.AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/', cartView.RemoveFromCartView.as_view(), name='cart-remove'),
    path('cart/update/', cartView.UpdateCartItemView.as_view(), name='cart-update'),

    path('orders/', orderView.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', orderView.OrderDetailView.as_view(), name='order-detail'),
    path('orders/checkout/', orderView.CheckoutView.as_view(), name='order-checkout'),

    path('shipments/', shipmentView.ShipmentListView.as_view(), name='shipment-detail'),
    path('shipments/<int:pk>/', shipmentView.ShipmentDetailView.as_view(), name='shipment-detail'),
]
