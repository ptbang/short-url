from rest_framework import serializers

from url_proxy.models import UrlProxy


class UrlProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlProxy
        fields = ['original', 'short']
        read_only_fields = ['short']


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlProxy
        fields = ['original', 'short']
        read_only_fields = ['original']
