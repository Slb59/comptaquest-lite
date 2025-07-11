from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from secretbox.dashboard.models import (CATEGORY_CHOICES, PERIODIC_CHOICES, PLACE_CHOICES,
                          PRIORITY_CHOICES, ColorParameter)
from tests.factories.colorparameters import ColorParameterFactory

class ColorParameterTests(TestCase):

    def setUp(self):
        self.valid_data = ColorParameterFactory(color="#123ABC")

    def test_create_color_parameter(self):
        param = ColorParameter.objects.create(**self.valid_data)
        self.assertEqual(ColorParameter.objects.count(), 1)
        self.assertEqual(param.color, "#123ABC")

    def test_unique_combination_constraint(self):
        ColorParameter.objects.create(**self.valid_data)
        with self.assertRaises(IntegrityError):
            ColorParameter.objects.create(**self.valid_data)

    def test_invalid_hex_color_raises_validation_error(self):
        invalid_data = self.valid_data.copy()
        invalid_data["color"] = "not-a-color"
        param = ColorParameter(**invalid_data)
        with self.assertRaises(ValidationError):
            param.full_clean()

    def test_str_method(self):
        param = ColorParameter.objects.create(**self.valid_data)
        self.assertIn(self.valid_data["priority"], str(param))
        self.assertIn(self.valid_data["color"], str(param))

    def test_get_color_parameter_coverage(self):
        total = len(PRIORITY_CHOICES) * len(PERIODIC_CHOICES) * len(CATEGORY_CHOICES) * len(PLACE_CHOICES)
        ColorParameter.objects.create(**self.valid_data)
        coverage = ColorParameter.get_color_parameter_coverage()
        self.assertTrue(coverage.startswith("1 /"))
        self.assertIn(f"{round(100 * 1 / total, 2)}%", coverage)
