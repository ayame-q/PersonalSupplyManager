from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
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
        fields = ("uuid", "type", "number", "category", "name", "manufacturer", "model", "serial_number", "length", "owner", "bought_at", "parent", "standards", "connectors", "connected_supplies", "position", "is_power_cable", "is_signal_cable", "is_active_cable", "note")
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "username")
        extra_kwargs = {
            'pk': {'read_only': True},
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "パスワードが一致しません"})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "現在のパスワードが間違っています"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
