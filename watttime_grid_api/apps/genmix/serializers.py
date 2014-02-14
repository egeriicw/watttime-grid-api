from apps.genmix.models import GenMix, Generation
from apps.gridentities.serializers import BalancingAuthoritySerializer
from rest_framework import serializers

class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    fuel = serializers.SlugRelatedField(slug_field='name')
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class GenMixSerializer(serializers.HyperlinkedModelSerializer):
    mix = GenerationSerializer(many=True)
    ba = BalancingAuthoritySerializer()

    class Meta:
        model = GenMix
        fields = ('ba', 'timestamp', 'created_at', 'confidence_type', 'url', 'mix')
        depth = 1
