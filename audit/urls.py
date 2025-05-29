from django.urls import path
from audit.views import logs_view

urlpatterns = [
    path('logs/', logs_view, name='logs_view'),
]
