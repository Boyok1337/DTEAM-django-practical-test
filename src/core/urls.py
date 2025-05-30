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
    path(
        "cv/<int:curriculum_id>/",
        views.CurriculumVitaeEmailPdf.as_view(),
        name="curriculum_vita_email_pdf"
    ),
    path(
        "cv/<int:curriculum_id>/translate/",
        views.translate_curriculum_vita_view,
        name="translate_curriculum_vita"
    ),
    path(
        "settings/",
        views.settings_view,
        name="settings"
    )
]
