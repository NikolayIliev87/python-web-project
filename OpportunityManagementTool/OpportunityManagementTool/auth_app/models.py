from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.db import models

from OpportunityManagementTool.auth_app.managers import OpportunityManagementToolUserManager
from OpportunityManagementTool.common.validators import validate_letters, validate_phone_number


class OpportunityManagementToolUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = OpportunityManagementToolUserManager()


class Manager(models.Model):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    user = models.OneToOneField(
        OpportunityManagementToolUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 25
    PHONE_MAX_LENGTH = 15
    GROUP_NAME_MAX_LENGTH = 20

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validate_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validate_letters,
        )
    )

    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        validators=(
            validate_phone_number,
        )
    )

    photo_url = models.URLField(
        null=True,
        blank=True,
    )

    is_manager = models.BooleanField()

    manager = models.EmailField(
        null=True,
        blank=True,
    )

    # manager = models.ForeignKey(
    #     Manager,
    #     on_delete=models.DO_NOTHING,
    #     primary_key=False,
    #     related_name='+',
    # )

    group = models.CharField(
        max_length=GROUP_NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    # group = models.ForeignKey(
    #     BusinessGroup,
    #     on_delete=models.DO_NOTHING,
    #     primary_key=False,
    #     related_name='+',
    #
    # )

    user = models.OneToOneField(
        OpportunityManagementToolUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
