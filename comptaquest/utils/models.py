from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Codification(models.Model):
    class CodeStatus(models.TextChoices):
        ACTIF = "Actif", "actif"
        INACTIF = "Inactif", "inactif"

    class CodeType(models.TextChoices):
        INCOME = "Income", "income"
        PAYMENT = "Payment", "payment"
        RESIDENCE = "Residence", "residence"
        HEALTH = "Health", "health"
        WATER = "Quality water", "quality water"
        CATEGORY = "Category", "category"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_codifications",
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    state = models.CharField(
        max_length=10, choices=CodeStatus.choices, default=CodeStatus.ACTIF
    )
    codetype = models.CharField(
        max_length=15, choices=CodeType.choices, default=CodeType.PAYMENT
    )


class PaymentCodificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(codetype=Codification.CodeType.PAYMENT)


class PaymentCodification(Codification):
    objects = PaymentCodificationManager()

    class Meta:
        proxy = True


class IncomeCodificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(codetype=Codification.CodeType.INCOME)


class IncomeCodification(Codification):
    class Meta:
        proxy = True

    objects = IncomeCodificationManager()


class CategoryCodificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(codetype=Codification.CodeType.CATEGORY)


class CategoryCodification(Codification):
    class Meta:
        proxy = True

    objects = CategoryCodificationManager()


class File(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_files",
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)


class Parameter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_parameters",
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    value = models.CharField(max_length=100)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = now()
        self.save()

    class Meta:
        abstract = True
