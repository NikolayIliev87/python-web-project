from django.contrib.auth import get_user_model
from django.db import models

from OpportunityManagementTool.common.validators import validate_phone_number

UserModel = get_user_model()


class BusinessGroup(models.Model):
    GROUP_NAME_MAX_LENGTH = 20

    name = models.CharField(
        max_length=GROUP_NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

    group = models.ForeignKey(
        BusinessGroup,
        on_delete=models.DO_NOTHING,
        primary_key=False,
        related_name='+',
    )

    price = models.FloatField()


class Client(models.Model):
    CLIENT_MAX_LENGTH = 25
    CITY_MAX_LENGTH = 20
    PHONE_MAX_LENGTH = 15

    name = models.CharField(
        max_length=CLIENT_MAX_LENGTH,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

    city = models.CharField(
        max_length=CITY_MAX_LENGTH,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        validators=(
            validate_phone_number,
        )
    )

    discount = models.IntegerField()


class Opportunity(models.Model):
    NAME_MAX_LENGTH = 25
    CLIENT_MAX_LENGTH = 20

    WON = 'Won'
    INPROGRESS = 'In Progress'
    OPEN = 'Open'
    LOST = 'Lost'

    TYPES = [(x, x) for x in (WON, INPROGRESS, OPEN, LOST)]
    TYPES_MAX_LENGTH = max([len(x) for x in (WON, INPROGRESS, OPEN, LOST)])

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    description = models.TextField(
        null=True,
        blank=True
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        primary_key=False,
        related_name='+',
        blank=True,
        null=True,
    )

    products = models.ManyToManyField(
        Product,
        through='OpportunityProducts',
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name='+',
    )

    close_date = models.DateField()

    status = models.CharField(
        max_length=TYPES_MAX_LENGTH,
        choices=TYPES,
    )

    newly_created = models.BooleanField(
        default=True
    )

    to_be_deleted = models.BooleanField(
        default=False
    )

    is_edite = models.BooleanField(
        default=False
    )

    # @property
    # def final_price(self):
    #     amount = sum([(i.price * i.id.) for i in self.products.all()])
    #
    #     return amount

    # @property
    # def size_tire(self):
    #     if self.final_price / 100 <= 0.1:
    #         return "0-10K"
    #     elif self.final_price / 100 <= 0.5:
    #         return "10K=50K"
    #     elif self.final_price / 100 <= 1.0:
    #         return "50K-100K"
    #     else:
    #         return "Above 100K"


class OpportunityProducts(models.Model):
    name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name='+',
    )

    def __str__(self):
        return self.name

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name='+',
    )

    quantity = models.IntegerField(
        default=1
    )

    @property
    def gross_price(self):
        amount = self.name.price * self.quantity

        return amount

    class Meta:
        unique_together = ('opportunity', 'name')
