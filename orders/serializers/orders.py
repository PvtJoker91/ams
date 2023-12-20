from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossierOrder
from orders.serializers.nested import UserOrderSerializer
from orders.serializers.utils import deadline


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        exclude = 'dossiers',


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = 'status', 'dossiers', 'close_reason', 'time_create', 'time_close'


class OrderListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()

    class Meta:
        model = DossierOrder
        fields = '__all__'

    def get_deadline(self, instance):
        return deadline(instance)


class OrderRetrieveSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    creator = UserOrderSerializer()
    dossiers = DossierSerializer(many=True)

    class Meta:
        model = DossierOrder
        fields = '__all__'

    def get_deadline(self, instance):
        return deadline(instance)


class OrderDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'
