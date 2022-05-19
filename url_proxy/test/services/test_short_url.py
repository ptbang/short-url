import string

from urllib.parse import urlparse
from django.test import TestCase

from url_proxy.models import UrlProxy
from url_proxy.services.short_url import (
    ShortUrlGenerator,
    ShortUrlGeneratorIterationExceededException,
)


class UrlProxyModelDataProviderTestMixin:
    def bulk_create_urls(self) -> None:
        urls = []
        chars = string.ascii_lowercase + string.digits
        for char in chars:
            urls.append(
                UrlProxy(
                    original=f'http://domain.com/loooooooooooooooooooog/{char}',
                    short=f'{UrlProxy.SHORT_URL_BASE}{char}/',
                )
            )
        UrlProxy.objects.bulk_create(urls)


class ShortUrlGeneratorTest(TestCase, UrlProxyModelDataProviderTestMixin):
    def test_get_short_url(self) -> None:
        short_url = ShortUrlGenerator.get_unique_short_url()
        url_parsed = urlparse(short_url)
        self.assertEqual(url_parsed.scheme, 'http')
        self.assertEqual(url_parsed.netloc, 'localhost:8000')

    def test_get_short_url_iterations_exceeded(self) -> None:
        self.bulk_create_urls()
        with self.assertRaises(ShortUrlGeneratorIterationExceededException):
            ShortUrlGenerator.get_unique_short_url(1)
