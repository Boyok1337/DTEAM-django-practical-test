from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api import views

router = DefaultRouter()
router.register(r'curriculum-vitae', views.CurriculumVitaeViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'contacts', views.ContactViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
