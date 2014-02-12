from apps.gridentities.models import GridEntity
from rest_framework import serializers


class GridEntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GridEntity
        fields = ('name', 'entity_type', 'url', 'abbrev')
