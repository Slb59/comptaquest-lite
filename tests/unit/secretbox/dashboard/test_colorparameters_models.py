from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from secretbox.dashboard.models import (CATEGORY_CHOICES, PERIODIC_CHOICES,
                                        PLACE_CHOICES, PRIORITY_CHOICES,
                                        ColorParameter)
from tests.factories.colorparameters import ColorParameterFactory


class ColorParameterTests(TestCase):

    def setUp(self):
        self.valid_data = ColorParameterFactory(
            priority="1-highest", periodic="01-none", place="partout", category="01-organisation", color="#123ABC"
        )

    def test_create_color_parameter(self):
        self.assertEqual(ColorParameter.objects.count(), 1)
        self.assertEqual(self.valid_data.color, "#123ABC")

    def test_unique_combination_constraint(self):
        with self.assertRaises(IntegrityError):
            ColorParameterFactory(
                priority="1-highest",
                periodicity="01-none",
                place="partout",
                category="01-organisation",
                color="#123ABC",
            )

    def test_invalid_hex_color_raises_validation_error(self):
        invalid_data = self.valid_data
        invalid_data.color = "not-a-color"
        with self.assertRaises(ValidationError):
            invalid_data.full_clean()

    def test_str_method(self):
        self.assertEqual(
            str(self.valid_data),
            f"{self.valid_data.priority} / {self.valid_data.periodic} / {self.valid_data.category} / {self.valid_data.place} → {self.valid_data.color}",
        )

    def test_get_color_parameter_coverage(self):
        total = len(PRIORITY_CHOICES) * len(PERIODIC_CHOICES) * len(CATEGORY_CHOICES) * len(PLACE_CHOICES)
        coverage = ColorParameter.get_color_parameter_coverage()
        self.assertTrue(coverage.startswith("1 /"))
        self.assertIn(f"{round(100 * 1 / total, 2)}%", coverage)
