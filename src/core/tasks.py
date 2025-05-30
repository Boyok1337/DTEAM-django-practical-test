from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from core.models import CurriculumVitae

from core.utils import PDFRenderer


@shared_task
def send_cv_pdf_email(email, cv_id):
    cv = CurriculumVitae.objects.get(id=cv_id)

    pdf_renderer = PDFRenderer("core/curriculum-vitae-detail-pdf.html", {"cv": cv})
    pdf_bytes = pdf_renderer.render()

    if pdf_bytes is None:
        return

    email_message = EmailMessage(
        subject="CV PDF",
        body="Please find your CV attached.",
        to=[email],
        from_email=settings.DEFAULT_FROM_EMAIL
    )

    email_message.attach('cv.pdf', pdf_bytes, 'application/pdf')
    email_message.send()
