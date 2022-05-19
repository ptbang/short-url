from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.serializers import UrlProxySerializer, ShortUrlSerializer
from url_proxy.models import UrlProxy
from url_proxy.services.short_url import ShortUrlGenerator


class ShortUrlView(CreateAPIView):
    serializer_class = UrlProxySerializer

    def perform_create(self, serializer: UrlProxySerializer) -> None:
        short = ShortUrlGenerator.get_unique_short_url()
        serializer.save(short=short)

    def create(self, request, *args, **kwargs):
        instance = UrlProxy.objects.filter(original=request.data.get('original')).first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return super().create(request, *args, **kwargs)


class OriginalUrlView(CreateAPIView):
    serializer_class = ShortUrlSerializer

    def create(self, request, *args, **kwargs):
        try:
            instance = UrlProxy.objects.get(short=request.data.get('short'))
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except UrlProxy.DoesNotExist:
            return Response({'detail': 'Given url does not exist.'}, status=status.HTTP_404_NOT_FOUND)
