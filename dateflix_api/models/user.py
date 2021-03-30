from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from dateflix_api.managers import UserManager

from .mixin import ModelMixin


class User(AbstractBaseUser, PermissionsMixin, ModelMixin):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    bio = models.TextField(_("bio"), blank=False, null=False)
    instagram = models.URLField(_("instagram"), blank=False, null=False)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, null=True, blank=True
    )
    birthday_date = models.DateField(_("birthday date"), null=True, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    instagram_user_id = models.CharField(
        _("instagram user id"), null=True, blank=True, max_length=20
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def short_name(self):
        return f"{self.first_name} {self.last_name[:1]}."

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.full_name
