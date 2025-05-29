from django.urls import path

from core import views

urlpatterns = [
    path(
        "",
        views.CurriculumVitaView.as_view(),
        name="curriculum_vitae_list"
    ),
    path(
        "cv/<int:curriculum_id>",
        views.CurriculumVitaDetailedView.as_view(),
        name="curriculum_vita_detailed"
    ),
    path(
        "cv/<int:curriculum_id>/pdf/",
        views.CurriculumVitaPDFView.as_view(),
        name="curriculum_vita_pdf"
    ),
]
