from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

from url_proxy.models import UrlProxy


class ViewTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.existing_url = UrlProxy.objects.create(
            original='http://example.com/first-loooooooooong-url',
            short='http://localhost:8000/0000/',
        )


class ShortUrlViewTest(ViewTestBase):
    API_URL = reverse('api:get-short-url')

    def test_post(self) -> None:
        original = 'http://example.com/loooooooooong-url'
        response = self.client.post(self.API_URL, data={'original': original})
        self.assertEqual(response.data['original'], original)

    def test_post_with_incorrect_original(self) -> None:
        original = 'example.com/loooooooooong-url'
        response = self.client.post(self.API_URL, data={'original': original})
        self.assertContains(
            response, 'Enter a valid URL.', status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_post_with_existing_original(self) -> None:
        response = self.client.post(
            self.API_URL, data={'original': self.existing_url.original}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original'], self.existing_url.original)
        self.assertEqual(response.data['short'], self.existing_url.short)


class OriginalUrlViewTest(ViewTestBase):
    API_URL = reverse('api:get-original-url')

    def test_success(self) -> None:
        response = self.client.post(
            self.API_URL, data={'short': self.existing_url.short}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original'], self.existing_url.original)

    def test_failed_with_non_existing_url(self) -> None:
        response = self.client.post(self.API_URL, data={'short': 'non-existing'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Given url does not exist.')
