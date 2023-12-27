from rest_framework import serializers

from archive.serializers.nested import DossierSerializer
from orders.models import DossiersOrder
from orders.serializers.nested import UserShortSerializer, TaskShortSerializer
from orders.serializers.utils import deadline


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossiersOrder
        exclude = 'dossiers',


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossiersOrder
        fields = 'status', 'dossiers', 'closer', 'close_reason', 'time_create', 'time_close'
        


class OrderListSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    tasks = TaskShortSerializer(many=True)

    class Meta:
        model = DossiersOrder
        fields = '__all__'

    def get_deadline(self, instance):
        return deadline(instance)


class OrderRetrieveSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    creator = UserShortSerializer()
    closer = UserShortSerializer()
    dossiers = DossierSerializer(many=True)

    class Meta:
        model = DossiersOrder
        fields = '__all__'

    def get_deadline(self, instance):
        return deadline(instance)


class OrderDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossiersOrder
        fields = 'id',
