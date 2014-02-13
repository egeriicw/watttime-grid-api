from apps.genmix.models import GenMix, Generation
from apps.gridentities.serializers import GridEntitySerializer
from rest_framework import serializers

class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class GenMixSerializer(serializers.HyperlinkedModelSerializer):
    sources = GenerationSerializer(many=True)
    ge = GridEntitySerializer()

    class Meta:
        model = GenMix
        fields = ('ge', 'timestamp', 'created_at', 'url', 'sources')
        depth = 1
