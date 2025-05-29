from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


class PDFRenderer:
    """
    Renders a Django HTML template with context to a PDF file using xhtml2pdf.
    """

    def __init__(self, template_path: str, context: dict = None):
        self.template_path = template_path
        self.context = context or {}

    def render(self) -> bytes | None:
        """
        Converts the rendered HTML template to PDF bytes.
        Returns:
            bytes: PDF content if successful, None otherwise.
        """
        template = get_template(self.template_path)
        html = template.render(self.context)
        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return result.getvalue()
        return None
