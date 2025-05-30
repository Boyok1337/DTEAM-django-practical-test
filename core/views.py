from django.shortcuts import render, get_object_or_404
from django.views import View

from core.models import CurriculumVitae


class CurriculumVitaView(View):
    def get(self, request):
        cvs = CurriculumVitae.objects.select_related(
            "contacts"
        ).prefetch_related(
            "skills",
            "projects"
        )
        context = {
            "cvs": cvs,
        }
        return render(request, "core/curriculum-vitae-list.html", context=context)


class CurriculumVitaDetailedView(View):
    def get(self, request, curriculum_id):
        cv = get_object_or_404(
            CurriculumVitae.objects.select_related(
                "contacts"
            ).prefetch_related(
                "skills",
                "projects"
            ),
            pk=curriculum_id
        )

        context = {
            "cv": cv,
        }
        return render(request, "core/curriculum-vitae-detail.html", context=context)
