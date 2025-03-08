from rest_framework import generics, permissions, status
from rest_framework.response import Response
from store.models import Shipment
from store.serializers import ShipmentSerializer


class ShipmentListView(generics.ListAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return Shipment.objects.filter(order__user=self.request.user)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipments not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class ShipmentDetailView(generics.RetrieveAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return Shipment.objects.filter(order__user=self.request.user)
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

