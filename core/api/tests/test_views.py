from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import CurriculumVitae, Skill, Project, Contact


class CurriculumVitaeAPITestCase(APITestCase):

    def setUp(self):
        self.contact = Contact.objects.create(
            type="email",
            contact_link="test@example.com"
        )
        self.skill = Skill.objects.create(name="Python")
        self.project = Project.objects.create(
            name="Test Project",
            description="A test project"
        )

    def test_create_cv_with_nested_data(self):
        """Test creating CV with all nested relationships"""
        url = reverse('curriculumvitae-list')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Software Developer',
            'contacts_data': {
                'type': 'email',
                'contact_link': 'john@example.com'
            },
            'skills_data': [
                {'name': 'Python'},
                {'name': 'Django'}
            ],
            'projects_data': [
                {
                    'name': 'Portfolio Website',
                    'description': 'Personal portfolio'
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify CV was created
        cv = CurriculumVitae.objects.get(id=response.data['id'])
        self.assertEqual(cv.first_name, 'John')
        self.assertEqual(cv.skills.count(), 2)
        self.assertEqual(cv.projects.count(), 1)

    def test_create_cv_with_existing_relations(self):
        """Test that existing relations are linked, not duplicated"""
        url = reverse('curriculumvitae-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'bio': 'Data Scientist',
            'contacts_data': {
                'type': 'email',
                'contact_link': 'test@example.com'  # This contact already exists
            },
            'skills_data': [
                {'name': 'Python'}  # This skill already exists
            ]
        }

        initial_contact_count = Contact.objects.count()
        initial_skill_count = Skill.objects.count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify no duplicates were created
        self.assertEqual(Contact.objects.count(), initial_contact_count)
        self.assertEqual(Skill.objects.count(), initial_skill_count)

    def test_update_cv_with_nested_data(self):
        """Test updating CV with nested data"""
        cv = CurriculumVitae.objects.create(
            first_name='Test',
            last_name='User',
            bio='Test Bio',
            contacts=self.contact
        )
        cv.skills.add(self.skill)

        url = reverse('curriculumvitae-detail', kwargs={'pk': cv.pk})
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'bio': 'Updated Bio',
            'skills_data': [
                {'name': 'JavaScript'},
                {'name': 'React'}
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cv.refresh_from_db()
        self.assertEqual(cv.first_name, 'Updated')
        self.assertEqual(cv.skills.count(), 2)
        self.assertTrue(cv.skills.filter(name='JavaScript').exists())

    def test_get_cv_list(self):
        """Test retrieving CV list"""
        cv = CurriculumVitae.objects.create(
            first_name='Test',
            last_name='User',
            bio='Test Bio',
            contacts=self.contact
        )

        url = reverse('curriculumvitae-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_cv_detail(self):
        """Test retrieving CV detail"""
        cv = CurriculumVitae.objects.create(
            first_name='Test',
            last_name='User',
            bio='Test Bio',
            contacts=self.contact
        )
        cv.skills.add(self.skill)
        cv.projects.add(self.project)

        url = reverse('curriculumvitae-detail', kwargs={'pk': cv.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(len(response.data['skills']), 1)
        self.assertEqual(len(response.data['projects']), 1)

    def test_delete_cv(self):
        """Test deleting CV"""
        cv = CurriculumVitae.objects.create(
            first_name='Test',
            last_name='User',
            bio='Test Bio',
            contacts=self.contact
        )

        url = reverse('curriculumvitae-detail', kwargs={'pk': cv.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CurriculumVitae.objects.filter(pk=cv.pk).exists())


class SkillAPITestCase(APITestCase):

    def setUp(self):
        self.skill = Skill.objects.create(name="Python")

    def test_create_skill(self):
        """Test creating a skill"""
        url = reverse('skill-list')
        data = {'name': 'React'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Skill.objects.filter(name='React').exists())
        self.assertEqual(response.data['name'], 'React')

    def test_get_skills_list(self):
        """Test retrieving skills list"""
        Skill.objects.create(name='Django')

        url = reverse('skill-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Python from setUp + Django

    def test_get_skill_detail(self):
        """Test retrieving skill detail"""
        url = reverse('skill-detail', kwargs={'pk': self.skill.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python')

    def test_update_skill(self):
        """Test updating a skill"""
        url = reverse('skill-detail', kwargs={'pk': self.skill.pk})
        data = {'name': 'Python 3.12'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, 'Python 3.12')

    def test_patch_skill(self):
        """Test partial update of skill"""
        url = reverse('skill-detail', kwargs={'pk': self.skill.pk})
        data = {'name': 'Python Advanced'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, 'Python Advanced')

    def test_delete_skill(self):
        """Test deleting a skill"""
        url = reverse('skill-detail', kwargs={'pk': self.skill.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_create_skill_duplicate_name(self):
        """Test creating skill with duplicate name"""
        url = reverse('skill-list')
        data = {'name': 'Python'}  # Already exists from setUp

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_skill_not_found(self):
        """Test 404 when skill doesn't exist"""
        url = reverse('skill-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProjectAPITestCase(APITestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="E-commerce Platform",
            description="Full-stack e-commerce solution"
        )

    def test_create_project(self):
        """Test creating a project"""
        url = reverse('project-list')
        data = {
            'name': 'Task Manager',
            'description': 'Project management application'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(name='Task Manager').exists())
        self.assertEqual(response.data['name'], 'Task Manager')

    def test_get_projects_list(self):
        """Test retrieving projects list"""
        Project.objects.create(
            name="Blog Platform",
            description="Content management system"
        )

        url = reverse('project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_project_detail(self):
        """Test retrieving project detail"""
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'E-commerce Platform')
        self.assertEqual(response.data['description'], 'Full-stack e-commerce solution')

    def test_update_project(self):
        """Test updating a project"""
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        data = {
            'name': 'Advanced E-commerce Platform',
            'description': 'Enterprise e-commerce solution with microservices'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Advanced E-commerce Platform')
        self.assertEqual(self.project.description, 'Enterprise e-commerce solution with microservices')

    def test_patch_project(self):
        """Test partial update of project"""
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        data = {'description': 'Updated description only'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        self.assertEqual(self.project.description, 'Updated description only')
        self.assertEqual(self.project.name, 'E-commerce Platform')  # Should remain unchanged

    def test_delete_project(self):
        """Test deleting a project"""
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_create_project_duplicate_name(self):
        """Test creating project with duplicate name"""
        url = reverse('project-list')
        data = {
            'name': 'E-commerce Platform',  # Already exists
            'description': 'Another e-commerce project'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_project_missing_required_fields(self):
        """Test validation for required fields"""
        url = reverse('project-list')
        data = {'name': 'Test Project'}  # Missing description

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)


class ContactAPITestCase(APITestCase):

    def setUp(self):
        self.contact = Contact.objects.create(
            type="email",
            contact_link="john@example.com"
        )

    def test_create_contact(self):
        """Test creating a contact"""
        url = reverse('contact-list')
        data = {
            'type': 'linkedin',
            'contact_link': 'https://linkedin.com/in/johndoe'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(type='linkedin').exists())
        self.assertEqual(response.data['type'], 'linkedin')

    def test_get_contacts_list(self):
        """Test retrieving contacts list"""
        Contact.objects.create(
            type="phone",
            contact_link="+1-555-0123"
        )

        url = reverse('contact-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_contact_detail(self):
        """Test retrieving contact detail"""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'email')
        self.assertEqual(response.data['contact_link'], 'john@example.com')

    def test_update_contact(self):
        """Test updating a contact"""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        data = {
            'type': 'email',
            'contact_link': 'john.doe@example.com'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.contact_link, 'john.doe@example.com')

    def test_patch_contact(self):
        """Test partial update of contact"""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        data = {'contact_link': 'updated@example.com'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.contact_link, 'updated@example.com')
        self.assertEqual(self.contact.type, 'email')  # Should remain unchanged

    def test_delete_contact(self):
        """Test deleting a contact"""
        url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_create_contact_missing_required_fields(self):
        """Test validation for required fields"""
        url = reverse('contact-list')
        data = {'type': 'email'}  # Missing contact_link

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact_link', response.data)


class IntegrationTestCase(APITestCase):
    """Test complete workflow scenarios"""

    def test_complete_cv_workflow(self):
        """Test complete CRUD workflow for CV"""
        create_url = reverse('curriculumvitae-list')
        create_data = {
            'first_name': 'Integration',
            'last_name': 'Test',
            'bio': 'Test workflow',
            'contacts_data': {
                'type': 'email',
                'contact_link': 'integration@test.com'
            },
            'skills_data': [
                {'name': 'Testing'},
                {'name': 'Integration'}
            ]
        }

        # CREATE
        create_response = self.client.post(create_url, create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        cv_id = create_response.data['id']

        # READ
        detail_url = reverse('curriculumvitae-detail', kwargs={'pk': cv_id})
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(detail_response.data['skills']), 2)

        # UPDATE
        update_data = {
            'first_name': 'Updated Integration',
            'last_name': 'Test',
            'bio': 'Updated workflow test',
            'skills_data': [
                {'name': 'Advanced Testing'}
            ]
        }
        update_response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        verify_response = self.client.get(detail_url)
        self.assertEqual(verify_response.data['first_name'], 'Updated Integration')
        self.assertEqual(len(verify_response.data['skills']), 1)

        # DELETE
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        verify_delete_response = self.client.get(detail_url)
        self.assertEqual(verify_delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_relationship_consistency(self):
        """Test that relationships are handled consistently"""
        # Create first CV with skills
        cv1_data = {
            'first_name': 'User1',
            'last_name': 'Test',
            'bio': 'First user',
            'contacts_data': {'type': 'email', 'contact_link': 'user1@test.com'},
            'skills_data': [{'name': 'Shared Skill'}]
        }

        response1 = self.client.post(reverse('curriculumvitae-list'), cv1_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Create second CV with same skill
        cv2_data = {
            'first_name': 'User2',
            'last_name': 'Test',
            'bio': 'Second user',
            'contacts_data': {'type': 'email', 'contact_link': 'user2@test.com'},
            'skills_data': [{'name': 'Shared Skill'}]  # Same skill name
        }

        response2 = self.client.post(reverse('curriculumvitae-list'), cv2_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Verify only one skill was created
        self.assertEqual(Skill.objects.filter(name='Shared Skill').count(), 1)

        # Verify both CVs reference the same skill
        skill = Skill.objects.get(name='Shared Skill')
        self.assertEqual(skill.curriculum_vitae.count(), 2)

