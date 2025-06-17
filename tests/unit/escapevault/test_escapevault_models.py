# from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from escapevault.models import NomadePosition
from tests.factories.nomadeposition import NomadePositionFactory


class NomadePositionTests(TestCase):

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



