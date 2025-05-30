from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from core.models import CurriculumVitae
from core.utils import PDFRenderer


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


class CurriculumVitaPDFView(View):
    """Generate and return a PDF version of the CV."""

    def get(self, request, curriculum_id):
        cv = CurriculumVitae.objects.select_related(
            "contacts"
        ).prefetch_related(
            "skills",
            "projects"
        ).get(pk=curriculum_id)

        pdf_renderer = PDFRenderer("core/curriculum-vitae-detail.html", {"cv": cv})
        pdf_content = pdf_renderer.render()

        if pdf_content:
            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="CV_{cv.first_name}_{cv.last_name}.pdf"'
            return response

        return HttpResponse("PDF generation failed", status=500)
