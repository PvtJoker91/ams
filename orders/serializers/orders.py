from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossierOrder
from orders.serializers.nested import UserOrderSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        exclude = 'dossiers',


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = 'status', 'dossiers', 'close_reason', 'time_create', 'time_close'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'


class OrderRetrieveSerializer(serializers.ModelSerializer):
    creator = UserOrderSerializer()
    dossiers = DossierSerializer(many=True)

    class Meta:
        model = DossierOrder
        fields = '__all__'


class OrderDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'
