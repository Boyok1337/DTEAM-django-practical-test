from rest_framework import serializers
from core.models import CurriculumVitae, Project, Skill, Contact


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'name',
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'type',
            'contact_link',
        )


class CurriculumVitaeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    contacts = ContactSerializer(read_only=True)

    # Write-only fields for nested creation/linking
    skills_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    projects_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    contacts_data = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = CurriculumVitae
        fields = [
            'id', 'first_name', 'last_name', 'bio', 'created_at', 'updated_at',
            'skills', 'projects', 'contacts',
            'skills_data', 'projects_data', 'contacts_data'
        ]

    def create(self, validated_data):
        skills_data = validated_data.pop('skills_data', [])
        projects_data = validated_data.pop('projects_data', [])
        contacts_data = validated_data.pop('contacts_data', None)

        contact = None
        if contacts_data:
            contact, created = Contact.objects.get_or_create(
                type=contacts_data['type'],
                contact_link=contacts_data['contact_link'],
                defaults=contacts_data
            )

        cv = CurriculumVitae.objects.create(contacts=contact, **validated_data)

        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            cv.skills.add(skill)

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults=project_data
            )
            cv.projects.add(project)

        return cv

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills_data', None)
        projects_data = validated_data.pop('projects_data', None)
        contacts_data = validated_data.pop('contacts_data', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if contacts_data:
            contact, created = Contact.objects.get_or_create(
                type=contacts_data['type'],
                contact_link=contacts_data['contact_link'],
                defaults=contacts_data
            )
            instance.contacts = contact

        instance.save()

        if skills_data is not None:
            instance.skills.clear()
            for skill_data in skills_data:
                skill, created = Skill.objects.get_or_create(
                    name=skill_data['name'],
                    defaults=skill_data
                )
                instance.skills.add(skill)

        if projects_data is not None:
            instance.projects.clear()
            for project_data in projects_data:
                project, created = Project.objects.get_or_create(
                    name=project_data['name'],
                    defaults=project_data
                )
                instance.projects.add(project)

        return instance
