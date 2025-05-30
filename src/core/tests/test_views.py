from django.test import TestCase, Client
from django.urls import reverse
from core.models import CurriculumVitae, Skill, Project, Contact


class CurriculumVitaViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("curriculum_vitae_list")

        self.contact = Contact.objects.create(type="email", contact_link="test@example.com")
        self.skill = Skill.objects.create(name="Python")
        self.project = Project.objects.create(name="Website", description="Portfolio site")

        self.cv = CurriculumVitae.objects.create(
            first_name="John",
            last_name="Doe",
            bio="Python developer",
            contacts=self.contact,
        )
        self.cv.skills.add(self.skill)
        self.cv.projects.add(self.project)

    def test_list_view_status_code(self):
        """Tests that the list view returns HTTP 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template_used(self):
        """Tests that the correct template is used for the list view."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/curriculum-vitae-list.html")

    def test_list_view_context(self):
        """Tests that the context in the list view contains the correct CV data."""
        response = self.client.get(self.url)
        cvs = response.context["cvs"]
        self.assertEqual(len(cvs), 1)
        self.assertEqual(cvs[0].first_name, "John")
        self.assertIn(self.skill, cvs[0].skills.all())


class CurriculumVitaDetailedViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact = Contact.objects.create(type="email", contact_link="jane@example.com")
        self.skill = Skill.objects.create(name="Django")
        self.project = Project.objects.create(name="API", description="Backend")

        self.cv = CurriculumVitae.objects.create(
            first_name="Jane",
            last_name="Doe",
            bio="Senior developer",
            contacts=self.contact,
        )
        self.cv.skills.add(self.skill)
        self.cv.projects.add(self.project)

        self.detail_url = reverse("curriculum_vita_detailed", kwargs={"curriculum_id": self.cv.pk})
        self.invalid_url = reverse("curriculum_vita_detailed", kwargs={"curriculum_id": 999})

    def test_detail_view_status_code(self):
        """Tests that the detail view returns HTTP 200 status for a valid CV."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        """Tests that the correct template is used for the detail view."""
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, "core/curriculum-vitae-detail.html")

    def test_detail_view_context(self):
        """Tests that the context in the detail view contains the correct CV details."""
        response = self.client.get(self.detail_url)
        context_cv = response.context["cv"]
        self.assertEqual(context_cv.first_name, "Jane")
        self.assertIn(self.skill, context_cv.skills.all())
        self.assertIn(self.project, context_cv.projects.all())

    def test_detail_view_not_found(self):
        """Tests that the detail view returns 404 or 500 when CV does not exist."""
        response = self.client.get(self.invalid_url)
        self.assertIn(response.status_code, [404, 500])
