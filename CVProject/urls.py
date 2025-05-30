from django.urls import path, include

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path("", include("core.api.urls")),
]
