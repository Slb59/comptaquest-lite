from django.core.exceptions import ValidationError
from django.test import TestCase

from tests.factories.nomadeposition import NomadePositionFactory
from escapevault.models import validate_city_format, validate_day_month_format

class TestNomadePosition(TestCase):

    def setUp(self):
        self.position = NomadePositionFactory()

    def test_create_position(self):
        """Test the basic creation of a position"""
        position = NomadePositionFactory(
            name="Nouvelle Position",
            stars=4,
            reviews=[{"rating": 4, "comment": "Bien"}],
            latitude=48.8576,
            longitude=2.3532,
        )

        self.assertEqual(position.name, "Nouvelle Position")
        self.assertEqual(position.country, "FR")
        self.assertEqual(position.stars, 4)
        self.assertEqual(len(position.reviews), 1)

    def test_coordinates_validation(self):
        """Test la validation des coordonnées"""
        # Test de latitude invalide
        with self.assertRaises(ValidationError):
            NomadePositionFactory(
                latitude=100,  # Latitude invalide
                longitude=2.3522,
            ).full_clean()

        # Test de longitude invalide
        with self.assertRaises(ValidationError):
            NomadePositionFactory(
                latitude=48.8566,
                longitude=200,  # Longitude invalide
            ).full_clean()

    def test_reviews_format(self):
        """Test le format des reviews"""
        position = NomadePositionFactory(
            name="Reviews Test",
            reviews=[{"rating": 5, "comment": "Excellent"}],
        )

        self.assertEqual(len(position.reviews), 1)
        self.assertEqual(position.reviews[0]["rating"], 5)

    def test_get_position_method(self):
        """Test la méthode get_position"""
        coords = self.position.get_position()
        self.assertEqual(coords, (self.position.latitude, self.position.longitude))

    def test_set_position_method(self):
        """Test la méthode set_position"""
        self.position.set_position(48.8586, 2.3542)
        self.assertEqual(self.position.latitude, 48.8586)
        self.assertEqual(self.position.longitude, 2.3542)

    def test_str_representation(self):
        """Test la représentation en chaîne du modèle"""
        expected = f"{self.position.name} ({self.position.city})"
        self.assertEqual(str(self.position), expected)

class TestValidateCityFormat(TestCase):
    def test_valid_city_names(self):
        valid_names = [
            "Paris",
            "New York",
            "São Paulo",
            "San-Francisco",
            "Lyon",
            "Aix en Provence",
            "Saint-Étienne"
        ]
        for name in valid_names:
            try:
                validate_city_format(name)
            except ValidationError:
                self.fail(f"validate_city_format() raised ValidationError unexpectedly for: '{name}'")

    def test_city_name_too_long(self):
        long_name = "A" * 41
        with self.assertRaises(ValidationError) as context:
            validate_city_format(long_name)
        self.assertIn("too long", str(context.exception))

    def test_city_name_with_invalid_characters(self):
        invalid_names = [
            "Paris!",
            "New_York",
            "San*Francisco",
            "123City",
            "City@Home",
            "Nantes.",
        ]
        for name in invalid_names:
            with self.assertRaises(ValidationError) as context:
                validate_city_format(name)
            self.assertIn("invalid characters", str(context.exception))

class ValidateDayMonthFormatTests(TestCase):
    def test_valid_dates(self):
        valid_values = [
            "01/01",
            "15/06",
            "31/12",
            "09/09",
            "30/04"
        ]
        for value in valid_values:
            try:
                validate_day_month_format(value)
            except ValidationError:
                self.fail(f"ValidationError raised unexpectedly for valid value: '{value}'")

    def test_invalid_dates_format(self):
        invalid_values = [
            "1/01",     # jour à un chiffre
            "01-01",    # séparateur invalide
            "32/01",    # jour trop grand
            "00/05",    # jour invalide
            "12/00",    # mois invalide
            "12/13",    # mois trop grand
            "aa/bb",    # lettres
            "31/4",     # mois à un chiffre
        ]
        for value in invalid_values:
            with self.assertRaises(ValidationError) as context:
                validate_day_month_format(value)
            self.assertIn("DD/MM", str(context.exception))