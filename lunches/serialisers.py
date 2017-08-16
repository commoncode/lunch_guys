from rest_framework import serializers

from lunches import models


class ItemSerialiser(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = ('title', 'description', 'stock', 'pk')


class OrderSerialiser(serializers.ModelSerializer):

    item = serializers.SlugRelatedField(
        queryset=models.Item.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = models.Order
        fields = ('name', 'item', 'pk')


class MenuSerialiser(serializers.ModelSerializer):

    items = ItemSerialiser(many=True)

    class Meta:
        model = models.Menu
        fields = ('day', 'items')
