from django.db.utils import IntegrityError
from django.test import TestCase
from url_proxy.models import UrlProxy


class UrlProxyTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.existing = UrlProxy.objects.create(
            original='http://existing.com/looooooooooong-url/',
            short='http://localhost:8000/0000/',
        )

    def test_create_success(self) -> None:
        original = 'http://domain.com/looooooooooong-url/'
        short = 'http://localhost:8000/abc1/'
        url = UrlProxy.objects.create(original=original, short=short)
        self.assertEqual(url.original, original)
        self.assertEqual(url.short, short)

    def test_create_failure_with_existing_original(self):
        with self.assertRaises(IntegrityError):
            UrlProxy.objects.create(
                original=self.existing.original, short='http://localhost:8000/1111/'
            )

    def test_create_failure_with_existing_proxy(self):
        with self.assertRaises(IntegrityError):
            UrlProxy.objects.create(
                original='http://domain.com/looooooooooong-url/',
                short=self.existing.short,
            )
