from django.test import TestCase, Client
from audit.models import RequestLog
from django.contrib.auth.models import User


class RequestLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='testpass')

    def test_request_logging_anonymous(self):
        self.client.get('/test-url/')
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.path, '/test-url/')
        self.assertIsNone(log.user)

    def test_request_logging_authenticated(self):
        self.client.login(username='test', password='testpass')
        self.client.get('/another-url/?q=abc')
        log = RequestLog.objects.first()
        self.assertEqual(log.user.username, 'test')
        self.assertEqual(log.query_string, 'q=abc')

    def test_logs_allowed_methods(self):
        self.client.get('/get-test/')
        self.client.post('/post-test/')
        self.client.put('/put-test/')
        self.client.delete('/delete-test/')
        methods = list(RequestLog.objects.values_list('method', flat=True))
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)

    def test_admin_and_logs_views_not_logged(self):
        self.client.get('/admin/')
        self.client.get('/logs/')
        self.assertEqual(RequestLog.objects.count(), 0)

    def test_remote_ip_logged(self):
        self.client.get('/ip-test/', REMOTE_ADDR='123.45.67.89')
        log = RequestLog.objects.first()
        self.assertEqual(log.remote_ip, '123.45.67.89')

    def test_query_string_logging(self):
        self.client.get('/search/?q=test&sort=asc')
        log = RequestLog.objects.first()
        self.assertEqual(log.query_string, 'q=test&sort=asc')

    def test_logged_in_user_attached(self):
        self.client.login(username='test', password='testpass')
        self.client.get('/user-check/')
        log = RequestLog.objects.first()
        self.assertEqual(log.user, self.user)

    def test_multiple_requests_logging(self):
        for i in range(20):
            self.client.get(f'/path-{i}/')
        self.assertEqual(RequestLog.objects.count(), 20)

    def test_timestamp_is_auto_created(self):
        self.client.get('/timestamp/')
        log = RequestLog.objects.first()
        self.assertIsNotNone(log.timestamp)

    def test_logging_on_404_not_found(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        log = RequestLog.objects.last()
        self.assertEqual(log.path, '/non-existent-url/')
        self.assertEqual(log.method, 'GET')
