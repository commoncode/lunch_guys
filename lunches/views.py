from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response

from . import models
from . import serialisers


class Menu(generics.ListAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = serialisers.MenuSerialiser


class MenuToday(generics.RetrieveAPIView):
    queryset = models.Menu.objects.all()
    serializer_class = serialisers.MenuSerialiser

    def retrieve(self, request, *args, **kwargs):
        today = timezone.datetime.today()
        try:
            instance = self.get_queryset().get(day=today)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Menu for {} has not been released".format(today.strftime("%d/%m/%y"))},
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class Item(generics.RetrieveAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serialisers.ItemSerialiser


class OrdersListCreate(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serialisers.OrderSerialiser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['item'].stock == 0:
            return Response({ 'status': "stock unavailable", 'data': serializer.data}, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data['item'].stock -= 1
        serializer.validated_data['item'].save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrdersDetail(generics.RetrieveDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serialisers.OrderSerialiser

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.item.stock += 1
        instance.item.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


