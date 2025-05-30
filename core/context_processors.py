from django.conf import settings


def settings_context(request):
    return {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'TIME_ZONE': settings.TIME_ZONE,
    }
