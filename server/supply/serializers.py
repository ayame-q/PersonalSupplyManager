from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Supply, Standard, Connector, SupplyConnectorRelation

class ConnectorField(serializers.ModelField):
    def __init__(self, *args, **kwargs):
        kwargs['source'] = '*'
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return value.get_connectors()

    def to_internal_value(self, data):
        return {self.field_name: data}


class SupplySerializer(serializers.ModelSerializer):
    connectors = ConnectorField(model_field=Supply)
    class Meta:
        model = Supply
        fields = ("uuid", "type", "number", "category", "name", "manufacturer", "model", "serial_number", "length", "owner", "bought_at", "parent", "standard", "connectors", "connected_supplies", "position", "is_power_cable", "is_signal_cable", "is_active_cable", "note")
        extra_kwargs = {
            'uuid': {'read_only': True},
            'type': {'read_only': True},
            'number': {'read_only': True},
        }

    def get_connectors(self, instance):
        return instance.get_connectors()

    def save(self, **kwargs):
        connectors = self.initial_data["connectors"]
        self.instance.set_connectors(connectors)
        deleted_connector_relations = self.instance.connector_relations.exclude(id__in=[connector["pk"] for connector in connectors if connector.get("pk")])
        deleted_connector_relations.delete()
        self.validated_data.pop("connectors")
        super(SupplySerializer, self).save(**kwargs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "username")
        extra_kwargs = {
            'pk': {'read_only': True},
        }


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class StandardSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    class Meta:
        model = Standard
        fields = ("pk", "name", "parent", "children")
        extra_kwargs = {
            'pk': {'read_only': True},
        }


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = ("pk", "name", "standard")
        extra_kwargs = {
            'pk': {'read_only': True},
        }
