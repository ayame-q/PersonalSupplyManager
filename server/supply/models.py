from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


# Create your models here.
class Standard(models.Model):
    name = models.CharField(max_length=40, verbose_name="名前")
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True, on_delete=models.SET_NULL, verbose_name="親規格")

    class Meta:
        ordering = ['parent__name', 'name']


class Connector(models.Model):
    name = models.CharField(max_length=40, verbose_name="名前")
    standard = models.ForeignKey(Standard, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="規格")


connector_genders = [
    ("None", "未定義"),
    ("Male", "オス"),
    ("Female", "メス")
]


class SupplyConnectorRelation(models.Model):
    connector = models.ForeignKey(Connector, related_name="supply_relations", on_delete=models.CASCADE, verbose_name="コネクタ")
    gender = models.CharField(choices=connector_genders, blank=True, null=True, max_length=10, verbose_name="オス・メス")
    supply = models.ForeignKey("Supply", related_name="connector_relations", on_delete=models.CASCADE, verbose_name="製品")
    count = models.IntegerField(default=1, verbose_name="個数")


types = [
    ("C", "ケーブル"),
    ("E", "電化製品")
]


class Supply(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=2, choices=types, verbose_name="分類")
    number = models.IntegerField(verbose_name="番号")
    category = models.CharField(max_length=40, blank=True, null=True, verbose_name="種類")
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name="名前")
    manufacturer = models.CharField(max_length=40, blank=True, null=True, verbose_name="メーカー")
    model = models.CharField(max_length=40, blank=True, null=True, verbose_name="型番")
    serial_number = models.CharField(max_length=200, blank=True, null=True, verbose_name="シリアルナンバー")
    length = models.IntegerField(blank=True, null=True, verbose_name="長さ(cm)")
    owner = models.ManyToManyField(get_user_model(), related_name="supplies", blank=True, verbose_name="所有者")
    bought_at = models.DateField(blank=True, null=True, verbose_name="購入日")
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True, on_delete=models.SET_NULL, verbose_name="本体")
    standard = models.ForeignKey(Standard, related_name="supplies", blank=True, null=True, on_delete=models.SET_NULL, verbose_name="規格")
    connectors = models.ManyToManyField(Connector, through=SupplyConnectorRelation, related_name="supplies", blank=True, verbose_name="コネクタ")
    connected_supplies = models.ManyToManyField("self", symmetrical=True, blank=True, verbose_name="接続先")
    position = models.TextField(blank=True, null=True, verbose_name="設置場所")
    is_power_cable = models.BooleanField(default=False, verbose_name="電源線か")
    is_signal_cable = models.BooleanField(default=False, verbose_name="信号線か")
    is_active_cable = models.BooleanField(default=False, verbose_name="アクティブケーブルか")
    note = models.TextField(null=True, blank=True, verbose_name="備考")
    created_at = models.DateTimeField(default=timezone.localtime, verbose_name="作成日")
    updated_at = models.DateTimeField(default=timezone.localtime, verbose_name="更新日")
    last_user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, verbose_name="最終更新者")

    def get_connectors(self):
        supply_connector_relations = self.connector_relations.all()
        return [{
            "pk": connector_relation.pk,
            "connector": connector_relation.connector.pk,
            "gender": connector_relation.gender,
            "count": connector_relation.count
        } for connector_relation in supply_connector_relations]

    def set_connectors(self, obj):
        for data in obj:
            connector = None
            if data.get("connector"):
                connector = Connector.objects.get(id=data.get("connector"))
            self.connector_relations.update_or_create(pk=data.get("pk"), connector=connector, gender=data.get("gender"), count=data.get("count"))