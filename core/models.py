from django.db import models

from base.models import BaseModel
from django.utils.translation import gettext_lazy as _


class CurriculumVitae(BaseModel):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    skills = models.ManyToManyField('Skill', related_name="curriculum_vitae")
    projects = models.ManyToManyField('Project', related_name="curriculum_vitae")
    bio = models.TextField(_("Biography"))
    contacts = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name="curriculum_vitae")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Skill(BaseModel):
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self):
        return f"{self.name}"


class Project(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))

    def __str__(self):
        return f"{self.name}"


class Contact(BaseModel):
    type = models.CharField(_("Type"), max_length=255)
    contact_link = models.CharField(_("Contact link"), max_length=255)

    def __str__(self):
        return f"{self.type} {self.contact_link}"
