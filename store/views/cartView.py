from rest_framework import generics, permissions, status
from rest_framework.response import Response
from store.models import Product, Cart, CartItem
from store.serializers import CartSerializer

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            return cart
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddToCartView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=product_id)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

            return Response({"message": "Product added to cart"})
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get('product_id')
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Product removed from cart"})
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        product_id = request.data.get('product_id')
        quantity_change = request.data.get('quantity_change')
        set_quantity = request.data.get('set_quantity')

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

            if set_quantity is not None:
                new_quantity = max(0, int(set_quantity))

            elif quantity_change is not None:
                new_quantity = max(0, cart_item.quantity + int(quantity_change))
            else:
                return Response({"error": "Provide either 'set_quantity' or 'quantity_change'."}, status=status.HTTP_400_BAD_REQUEST)

            if new_quantity == 0:
                cart_item.delete()
                return Response({"message": "Cart item removed from cart"}, status=status.HTTP_200_OK)

            cart_item.quantity = new_quantity
            cart_item.save()
            return Response({"message": "Cart item updated", "new_quantity": cart_item.quantity})

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid quantity input"}, status=status.HTTP_400_BAD_REQUEST)