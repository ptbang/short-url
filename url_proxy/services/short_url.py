import random, string

from url_proxy.models import UrlProxy


class ShortUrlGenerator:
    MAX_NUM_ITERATIONS = 1000
    UNIQUE_STR_DEFAULT_LEN = 4

    @classmethod
    def get_unique_short_url(cls, key_len: int = UNIQUE_STR_DEFAULT_LEN) -> str:
        unique = False
        for i in range(cls.MAX_NUM_ITERATIONS):
            short_url = f'{UrlProxy.SHORT_URL_BASE}{cls._get_radom_string(key_len)}/'
            if not UrlProxy.objects.filter(short=short_url).count():
                unique = True
                break
        if unique:
            return short_url
        else:
            raise ShortUrlGeneratorIterationExceededException(
                f'Max number of iterations {cls.MAX_NUM_ITERATIONS} exceeded'
            )

    @staticmethod
    def _get_radom_string(key_len: int) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=key_len))


class ShortUrlGeneratorIterationExceededException(Exception):
    pass
