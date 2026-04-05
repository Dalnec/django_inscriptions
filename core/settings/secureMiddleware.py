from django.conf import settings
from rest_framework.renderers import JSONRenderer
from urllib.parse import urlparse, urlunparse
import platform


class BaseUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.is_secure():
            scheme = 'https'
        else:
            scheme = 'http'

        # Configuración de la URL base
        request.base_url = f"{scheme}://{request.get_host()}"

        # Configuración de la URL de los medios y estáticos
        request.media_url = f"{scheme}://{request.get_host()}{settings.MEDIA_URL}"
        request.static_url = f"{scheme}://{request.get_host()}{settings.STATIC_URL}"

        return self.get_response(request)


def convert_url_to_https(request,url):
    parsed = urlparse(url)
    operating_system = platform.system()

    if operating_system == 'Linux':
        if parsed.scheme == 'http':
            parsed = parsed._replace(scheme='https')
            return urlunparse(parsed)
    else:
        if parsed.scheme == 'http':
            parsed = parsed._replace(scheme='http')
            return urlunparse(parsed)
    return url


def update_urls(data, request, scheme='https'):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = key
            if isinstance(key, str):
                new_key = convert_url_to_https(request,key)
            new_value = update_urls(value, request, scheme)
            new_data[new_key] = new_value
        return new_data

    elif isinstance(data, list):
        new_data = []
        for item in data:
            new_item = update_urls(item, request, scheme)
            new_data.append(new_item)
        return new_data

    else:
        if isinstance(data, str):
            return convert_url_to_https(request,data)
        else:
            return data


class HTTPSRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get('request')
        scheme = 'https'

        data = update_urls(data, request, scheme)

        return super().render(data, accepted_media_type, renderer_context)

