from django.contrib import admin
from .models import Supply, Standard, Connector, SupplyConnectorRelation

# Register your models here.
admin.site.register(Supply)
admin.site.register(Standard)
admin.site.register(Connector)
admin.site.register(SupplyConnectorRelation)
