# Generated by Django 5.2.1 on 2025-05-21 15:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Codification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(blank=True, max_length=300)),
                (
                    "state",
                    models.CharField(
                        choices=[("Actif", "actif"), ("Inactif", "inactif")], default="Actif", max_length=10
                    ),
                ),
                (
                    "codetype",
                    models.CharField(
                        choices=[
                            ("Income", "income"),
                            ("Payment", "payment"),
                            ("Residence", "residence"),
                            ("Health", "health"),
                            ("Quality water", "quality water"),
                            ("Category", "category"),
                        ],
                        default="Payment",
                        max_length=15,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_codifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CategoryCodification",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("utils.codification",),
        ),
        migrations.CreateModel(
            name="IncomeCodification",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("utils.codification",),
        ),
        migrations.CreateModel(
            name="PaymentCodification",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("utils.codification",),
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(blank=True, max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("path", models.CharField(max_length=200)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Parameter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(blank=True, max_length=300)),
                ("value", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_parameters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
