from audit.models import RequestLog
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/logs/'):
            return

        ip = request.META.get('REMOTE_ADDR')

        RequestLog.objects.create(
            method=request.method,
            path=request.path,
            query_string=request.META.get('QUERY_STRING', ''),
            remote_ip=ip,
            user=request.user if request.user.is_authenticated else None
        )
