import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django_cities_light.models import City
from django_countries.fields import Country
from .models import NomadePosition
import uuid

@pytest.mark.django_db
class NomadePositionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'une ville de test
        cls.test_city = City.objects.create(
            name='Paris',
            country_id='FR'
        )
        
        # Création d'une position de test
        cls.position = NomadePosition.objects.create(
            name='Test Position',
            address='123 rue de Test',
            city=cls.test_city,
            country='FR',
            stars=5,
            reviews=[{'rating': 5, 'comment': 'Excellent'}],
            opening_date='2025-01-01',
            closing_date='2025-12-31',
            category='Restaurant',
            latitude=48.8566,
            longitude=2.3522
        )

    def test_create_position(self):
        """Test la création basique d'une position"""
        position = NomadePosition.objects.create(
            name='Nouvelle Position',
            address='456 rue de Test',
            city=self.test_city,
            country='FR',
            stars=4,
            reviews=[{'rating': 4, 'comment': 'Bien'}],
            opening_date='2025-01-01',
            category='Café',
            latitude=48.8576,
            longitude=2.3532
        )
        
        self.assertEqual(position.name, 'Nouvelle Position')
        self.assertEqual(position.stars, 4)
        self.assertEqual(len(position.reviews), 1)
        self.assertIsNotNone(position.id)

    def test_uuid_generation(self):
        """Test que l'UUID est généré automatiquement"""
        position = NomadePosition.objects.create(
            name='Test UUID',
            address='789 rue de Test',
            city=self.test_city,
            country='FR'
        )
        self.assertIsInstance(position.id, uuid.UUID)

    def test_coordinates_validation(self):
        """Test la validation des coordonnées"""
        # Test de latitude invalide
        with self.assertRaises(ValidationError):
                       NomadePosition.objects.create(
                name='Invalid Lat',
                address='Test',
                city=self.test_city,
                country='FR',
                latitude=100,  # Latitude invalide
                longitude=2.3522
            ).full_clean()

        # Test de longitude invalide
        with self.assertRaises(ValidationError):
            NomadePosition.objects.create(
                name='Invalid Lon',
                address='Test',
                city=self.test_city,
                country='FR',
                latitude=48.8566,
                longitude=200  # Longitude invalide
            ).full_clean()

    def test_reviews_format(self):
        """Test le format des reviews"""
        position = NomadePosition.objects.create(
            name='Reviews Test',
            address='Test',
            city=self.test_city,
            country='FR',
            reviews=[{'rating': 5, 'comment': 'Excellent'}]
        )
        
        self.assertEqual(len(position.reviews), 1)
        self.assertEqual(position.reviews[0]['rating'], 5)

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

class NomadePositionAdminTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(self.admin_user)
        self.position = NomadePosition.objects.create(
            name='Test Admin',
            address='Test Address',
            city=City.objects.create(name='Lyon', country_id='FR'),
            country='FR'
        )

    def test_admin_export_csv(self):
        """Test l'export CSV depuis l'interface admin"""
        response = self.client.post(f'/admin/nomades/nomadeposition/{self.position.id}/export_to_csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')