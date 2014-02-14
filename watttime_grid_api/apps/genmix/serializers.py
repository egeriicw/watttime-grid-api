from apps.genmix.models import GenMix, Generation
from apps.gridentities.serializers import BalancingAuthoritySerializer
from rest_framework import serializers

class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class GenMixSerializer(serializers.HyperlinkedModelSerializer):
    sources = GenerationSerializer(many=True)
    ba = BalancingAuthoritySerializer()

    class Meta:
        model = GenMix
        fields = ('ba', 'timestamp', 'created_at', 'confidence_type', 'url', 'sources')
        depth = 1
