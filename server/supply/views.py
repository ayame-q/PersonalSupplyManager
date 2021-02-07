from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from .serializers import SupplySerializer, UserSerializer, StandardSerializer, ConnectorSerializer
from .models import Supply, Standard, Connector, types as supply_types
import re


# Create your views here.
class SupplyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


class SupplySearchAPIView(ListAPIView):
    serializer_class = SupplySerializer
    def get_queryset(self):
        full_number = self.request.GET.get("full_number")
        if self.kwargs.get("full_number"):
            full_number = self.kwargs.get("full_number")
        match = re.fullmatch(r"([A-Z]{1,3})([0-9]+)", full_number)
        supply_type = match.group(1)
        number = int(match.group(2))
        return Supply.objects.filter(type=supply_type, number=number)


class SupplyCreateAPIView(APIView):
    def post(self, request):
        supply_type = request.data.get("type")
        if not supply_type in [supply_type[0] for supply_type in supply_types]:
            raise ValidationError("type is inValid")
        count = request.data.get("count")
        try:
            count = int(count)
        except:
            raise ValidationError("count is inValid")
        if count < 0:
            raise ValidationError("count is inValid")
        newest_supply = Supply.objects.filter(type=supply_type).order_by("-number").first()
        start_number = newest_supply.number + 1 if newest_supply else 1
        supplies = []
        for i in range(start_number, start_number + count):
            supply = Supply.objects.create(type=supply_type, number=i)
            supplies.append({"uuid": supply.uuid, "type": supply.type, "number": supply.number})
        return Response(supplies)


class UserListAPIView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class StandardListCreateAPIView(ListCreateAPIView):
    queryset = Standard.objects.filter(parent=None).order_by("name")
    serializer_class = StandardSerializer


class StandardRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer


class ConnectorListCreateAPIView(ListCreateAPIView):
    queryset = Connector.objects.order_by("standard__name", "name")
    serializer_class = ConnectorSerializer


class ConnectorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Connector.objects.all()
    serializer_class = ConnectorSerializer
