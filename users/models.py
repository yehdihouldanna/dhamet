from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Project."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    phone = models.CharField(verbose_name=_("Phone"), max_length=20, blank=False)

    def __str__(self):
        return f"{self.username}: {self.phone}"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = []
        permissions = [
            ("add_user", _("Can add user")),
            ("view_user", _("Can view user")),
            ("change_user", _("Can change user")),
            ("delete_user", _("Can delete user")),
            ("list_user", _("Can list users")),
        ]

    def get_update_url(self):
        return reverse("users:update", kwargs={"pk": self.pk})
